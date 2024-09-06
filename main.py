import os
from dotenv import load_dotenv
import openai
import streamlit as st
from langchain import hub
from openai import OpenAI
from pinecone import Pinecone
from sqlalchemy import create_engine
import base64
from audio_recorder_streamlit import audio_recorder

import json
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import AgentExecutor, create_openai_functions_agent

from sqlalchemy import MetaData, create_engine
from funcs import init_memory, create_human_readable_response, make_topic_name
from prompts import agent_prompt_with_history, agent_prompt_without_history, find_top_k_nearest_examples
from plotly.io import read_json as plotly_read_json
import plotly.io as pio
import uuid
from configs.table_info import table_info
import time 


load_dotenv()


pinecone_index = '#'
pinecone_namespace = '#'

gpt_model = '#' 
OPENAI_API_KEY = '#' 

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY


# Initialize LLM
llm = ChatOpenAI(model=gpt_model, temperature=0, openai_api_key=OPENAI_API_KEY)

# Memory Params
memory_params = {'llm': llm, 'memory_type': 'window', 'max_token_limit': 2000, 'k': 1}

client = OpenAI(api_key='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')

pinecone_client = Pinecone(api_key="5ec49a0d-4e4f-4d9c-9cee-1786a045970e")
index = pinecone_client.Index(pinecone_index)

st.set_page_config(page_title="SQL - DBTalk ", layout="wide")


@st.cache_resource
def db_init():
    service_account_file = "service-account-key.json" # Change to where your service account key file is located

    project = "#
    dataset = "dt_maven_sample_datasets"
    table = ["sample_data_sales_dnk","sample_data_marketing_dnk"]
    sqlalchemy_url = f'bigquery://{project}/{dataset}?credentials_path={service_account_file}'

    engine = create_engine(sqlalchemy_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    db = SQLDatabase(engine = engine,
                      include_tables = table,
                    )
    return db

def transcribe_audio(client, audio_path):
    with open(audio_path,"rb") as audio_file:
        transcript = client.audio.transcriptions.create(model = "whisper-1", file = audio_file)
        return transcript.text





# Initialize database,memory and db_chain in session_state
if 'db_init' not in st.session_state:
    print("INIT DATABASE")
    st.session_state.db_init = db_init()
    print("DATABASE INIT COMPLETED")

if "memory" not in st.session_state:
    st.session_state.memory = init_memory(**memory_params)

if "db_chain" not in st.session_state:
    st.session_state.db_chain = SQLDatabaseChain.from_llm(llm,
                                                          db=st.session_state.db_init,
                                                          memory=st.session_state.memory,
                                                          verbose=True,
                                                          use_query_checker=True,
                                                          top_k=100,
                                                          return_sql=True
                                                          )


# Create the chain
def create_chain():
    st.session_state.memory = init_memory(**memory_params)
    st.session_state.db_chain = SQLDatabaseChain.from_llm(llm,
                                                          db=st.session_state.db_init,
                                                          memory=st.session_state.memory,
                                                          verbose=True,
                                                          use_query_checker=True,
                                                          top_k=100,
                                                          return_sql=True
                                                          )


# Run query with retries
def run_query_with_retries(query, max_retries=10):
    few_short_examples = find_top_k_nearest_examples(user_query=query,
                                                     open_ai_client=client,
                                                     pinecone_client=pinecone_client,
                                                     pinecone_index_name="fewshortexamples",
                                                     pinecone_namespace_name='ns1')
    attempt = 0
    last_error = None
    while attempt < max_retries:
        try:
            if st.session_state.memory and st.session_state.memory.load_memory_variables({})['history']:
                history = st.session_state.memory.load_memory_variables({})['history']
                agent_prompt = agent_prompt_with_history(history=history,
                                                         query=query,
                                                         few_short_examples=few_short_examples,
                                                         error=last_error)
            else:
                agent_prompt = agent_prompt_without_history(query=query, few_short_examples=few_short_examples)
            result = st.session_state.db_chain.invoke(agent_prompt)
            result = json.loads(result["result"])
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("Generated SQL QUERY : \n ", result["SQL_Query"])
            db = st.session_state.db_init
            result["SQL_Result"] = db.run(result["SQL_Query"], include_columns=True)
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

            print("Generated Response from API : \n ",result)
            print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

            return result
        except Exception as current_error:
            attempt += 1
            last_error = current_error
            st.warning(f"Attempt {attempt} failed with error: {current_error}")
            if attempt >= max_retries:
                raise current_error


def viz_prompt(json_response, chart_type):
    if chart_type == None:
        return f"""
            <Objective>
            You are a highly intelligent data analyst specialising in data visualisation using python
            based on the understanding the user requirements.
            Your task is to understand the user query, llm thougut, analysis code, analysis results
            and natural language summary to write python code to create an appropriate user friendly chart using plotly.
            The graph should be saved as plotly.write_json() file with a unique name {uuid.uuid4()}.

            - Always write good python code.
            - Do not create mock data or sample data on your own.
            - Always import the correct libraries before using them.
            - Always consider year, month, quarters as categorical variables.
            - Do not use more than 10 classes in the color variable.
            - Be mindful of the data to be plotted and come up with an appropriate plot type unless specified by the user.
            - Use barmode as group whenever creating a barchart.
            - Always mention an appropriate title to the plot
            - Always mention the appropriate label on the x and y axis
            - If x axis shows years/months etc make sure they appear as strings
            - Use plotly_dark theme as the plot theme and
            - If using colours for qualitative use the the color sequences of ["Set3", "Pastel2"]
            - If using colours for continuous scale use **blues**
            
            </Objective>
            <Caution>
            Never use python libraries like subprocess, os, sys as it can interfere with my system.
            </Caution>
            While Plotting the following Analysis Results Do consider to comply with the user query.
            <User Query>
            {json_response["user_query"]}
            </User Query>

            <Analysis Results>
            {json_response["SQL_Result"]}
            </Analysis Results>
            ***If the analysis results are empty, create an empty chart and ensure no mock data is assumed. Only return the name of the file and nothing else.***
            
            ***The graph should be saved as plotly.write_json() file with a unique name.
            Only return the name of the file and nothing else
            <Output Format/>
            Output:
            """
    else:
        return f"""
            <Objective>
            You are a highly intelligent data analyst specialising in data visualisation using python
            based on the understanding the user requirements.
            Your task is to understand the user query, llm thougut, analysis code, analysis results
            and natural language summary to write python code to create an appropriate user friendly chart using plotly.
            The graph should be saved as plotly.write_json() file with a unique name {uuid.uuid4()}.
            Plot {chart_type} according to following below guidelines.
            - Always write good python code.
            - Always import the correct libraries before using them.
            - Do not create mock data or sample data on your own.
            - Always consider year, month, quarters as categorical variables.
            - Do not use more than 10 classes in the color variable.
            - Be mindful of the data to be plotted and come up with an appropriate plot type unless specified by the user.
            - Use barmode as group whenever creating a barchart.
            - Always mention an appropriate title to the plot
            - Always mention the appropriate label on the x and y axis
            - If x axis shows years/months etc make sure they appear as strings
            - Use plotly_dark theme as the plot theme and
            - If using colours for qualitative use the the color sequences of ["Set3", "Pastel2"]
            - If using colours for continuous scale use **blues**
            
            </Objective>
            <Caution>
            Never use python libraries like subprocess, os, sys as it can interfere with my system.
            </Caution>
            While Plotting the following Analysis Results Do consider to comply with the user query.
            <User Query>
            {json_response["user_query"]}
            </User Query>

            <Analysis Results>
            {json_response["SQL_Result"]}
            </Analysis Results>
            ***If the analysis results are empty, create an empty chart and ensure no mock data is assumed. Only return the name of the file and nothing else.***
            
            ***The graph should be saved as plotly.write_json() file with a unique name.
            Only return the name of the file and nothing else
            <Output Format/>
            Output:
            """


def create_plot(response_json, chart_type=None):
    tool = [PythonREPLTool()]
    viz_prompt_with_response = viz_prompt(json_response=response_json,
                                          chart_type=chart_type)
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=viz_prompt_with_response)
    agent = create_openai_functions_agent(ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model='gpt-4o-mini'),
                                          tool, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True, handle_parsing_errors=True, required=True)
    viz_response = agent_executor.invoke({"input": f"plot {response_json}"})
    viz_file_name = viz_response["output"]

    if os.path.isfile(viz_file_name):
        with open(viz_file_name, 'r') as file:
            json_content = file.read()
    else:
        raise FileNotFoundError(f"File {viz_file_name} does not exist.")

    plotly_fig = pio.from_json(json_content)
    os.remove(viz_file_name)
    return plotly_fig

################## dataframe agent ###################

def sql_df_prompt(sql_results):
    return f"""
        <Objective>
        You are a highly intelligent BigQuery results to DataFrame converter specializing in using Python.
        Your task is to return the DataFrame as a dictionary format using df.to_dict().

        - Always write good Python code.
        - Do not create mock data or sample data on your own.
        - Always import the correct libraries before using them.
        
        </Objective>
        <Caution>
        Never use Python libraries like subprocess, os, sys as it can interfere with my system.
        </Caution>

        <Analysis Results>
        {sql_results}
        </Analysis Results>
        ***If the analysis results are empty, create an empty dictionary.***

        Output should be in the format of df.to_dict() from pandas DataFrame.
    """
    
def create_dataframe_out_of_sql_result(sql_result):
    tool = [PythonREPLTool()]
    prompt_with_response = sql_df_prompt(sql_result)
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=prompt_with_response)
    agent = create_openai_functions_agent(ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model='gpt-4o-mini'),
                                          tool, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool, verbose=True, handle_parsing_errors=True, required=True)
    response = agent_executor.invoke({"input": f"{sql_result}"})

    return response



def response_chain(query, few_shot_examples = None):
    response_json = run_query_with_retries(query, max_retries=10)
    response = create_human_readable_response(resp=response_json, openai_model=gpt_model)
    response_json["human_language"] = response
    return response_json


# Streamlit interface
st.sidebar.image("assets/dt_logo_slim-trans-small.png", use_column_width=True)
st.sidebar.divider()


action = st.sidebar.radio(label="**Select Action**",
                          options=[':rainbow[Talk to Data]',
                                   # 'Visualise my Data',
                                   # 'Explore Data Schemas'
                                   ],
                          captions=[":rainbow[Query data in natural language]",
                                    "Use Natural language to create charts",
                                    "Explore tables available for AI"],
                          horizontal=False)
st.sidebar.divider()


if "audio_text" not in st.session_state:
    st.session_state.audio_text = None

with st.sidebar:
    recorded_audio = audio_recorder()
    if recorded_audio:
        audio_file = "audio.mp3"
        with open(audio_file, "wb") as f:
            f.write(recorded_audio)
        transcribed_text = transcribe_audio(client=client, audio_path=audio_file)
        print(transcribed_text)
        st.session_state.audio_text = transcribed_text
        st.write(transcribed_text)

if action == ':rainbow[Talk to Data]':
    first_message = {"role": "assistant", "content": "Hi, How can I help you today?"}
    from pandas import Timestamp
    if st.sidebar.button("Initiate new conversation"):
        create_chain()
        st.session_state.messages = [first_message]

    if 'messages' not in st.session_state:
        st.session_state.messages = [first_message]
        session_history_messages = {}

    # Display previous messages
    for message in st.session_state.messages:
        if message["role"] == 'assistant':
            with st.chat_message(message["role"], avatar="🦾"):
                try:
                    result = message["content"]

                    with st.expander("**LLM Thought**"):
                        st.markdown(result["llm_thoughts"])

                    with st.expander("**SQL Query**"):
                        st.markdown(result["SQL_Query"])

                    with st.expander("**Data Results**"):
                        st.markdown(result["SQL_Result"])
                    st.markdown(result["human_language"])
                    
                    st.plotly_chart(result['viz'], use_container_width=True, width=800, height=600)
                    st.write(result["time_taken"])
                except Exception as e:
                    st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar="👨🏻‍💼"):
                st.markdown(message["content"])

   
    if st.session_state.audio_text:
        query = st.session_state.audio_text
        st.session_state.audio_text = None  
    else:
        query = st.chat_input("Begin here to chat with your data")
    
    if query:
        start = Timestamp("now")

        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user", avatar="👨🏻‍💼"):
            print("inside chatbox", st.session_state.audio_text)
            st.markdown(query)

        with st.chat_message("assistant", avatar="🦾"):

            result = response_chain(query)

            with st.expander("**LLM Thought**"):
                st.markdown(result["llm_thoughts"])

            with st.expander("**SQL Query**"):
                st.markdown(result["SQL_Query"])
            viz_result = create_plot(response_json=result)

            def stream_data():
                import time
                for word in result["human_language"].split(" "):
                    yield word + " "
                    time.sleep(0.05)
            stream_data

            result['viz'] = viz_result
            # result_df = create_dataframe_out_of_sql_result(sql_result=result["SQL_Result"])
            # st.write(result_df)
            # result_df = convert_sql_result_to_dataframe(result["SQL_Result"])
            # print(sql_result)
            # print("---------------------Enter------------------------------------------")
            # result_df = bg_db.read_data_gbq_native_client(query=result["SQL_Query"])
            # print("---------------------Exit------------------------------------------")
            # st.dataframe(result_df)

            st.plotly_chart(viz_result, use_container_width=True, width=800, height=600)
            result["time_taken"] = Timestamp("now") - start
            st.write(result["time_taken"])
        st.session_state.messages.append({"role": "assistant", "content": result})

    if len(st.session_state.messages) > 1:
        st.markdown("<div style='text-align: center; margin-top: 10px; color: grey;'>Like humans, AI can also make mistakes, but together we can achieve excellence</div>", unsafe_allow_html=True)

    
suggested_questions = [
    "Which sales channels are performing best in terms of revenue across different platforms?",
    "What is the relationship between the advertising spend and revenue generated for each product category?",
 "How do conversion rates vary by country for different marketing campaigns?",
    "What are the most popular products based on sales and impressions in various regions?",
     "How does the discount applied to orders correlate with the marketing spend for each advertising campaign?",  ###### join 
  "What is the impact of different advertising campaigns on sales across various countries?",
     "Which product groups have the highest revenue and spend across different ad groups?",
    "What are the average impressions and clicks for each product group in different sales channels?",
     "How do the revenues for different product brands compare to their advertising spend?", ######### join
    "What are the trends in sales and advertising spend over time for specific marketing campaigns?" ########## join
    ,
     "Which customer segments show the highest response rates to specific marketing campaigns?", 
     "How do shipping costs impact the effectiveness of different ad groups in generating revenue?", ####### join
     "What is the correlation between the number of impressions and the number of items sold for different product categories?", ####### join
     "Which promotions are most effective in driving sales through specific sales channels?",
    "How do order statuses vary across different advertising campaigns and sales channels?",
    "What is the average order value for each sales channel and how does it relate to the ad spend?",
    "Which geographic regions generate the highest revenue for specific marketing campaigns?",
     "How does the time of day impact the success of marketing campaigns in terms of sales and clicks?",
     "What is the relationship between customer types (new vs. repeat) and their response to marketing campaigns?",
    "Which products have the highest return rates and how do they correlate with the marketing spend?",
    ########################################## New Questions ############################################

    "What is the total revenue generated by specific sales channels for products that were part of a particular ad campaign?",
    "Which sales channels had the highest conversion rates during promotions and how does this compare across different countries?",
    "How does the average discount offered in a specific ad group correlate with the increase in product revenue across different sales channels?",
    "What is the impact of ad spend on the revenue of new versus repeat customers across various sales channels?",
    "Which product categories saw the highest revenue growth during a specific ad campaign, and what were the associated promotion details?",
    "What is the correlation between the number of impressions and the final revenue across different regions for specific products?",
    "How did different customer types (new vs. repeat) respond to various ad campaigns in terms of revenue generated?",
    "What is the relationship between ad spend and average order value across different sales channels?",
    "Which geographic regions saw the highest conversion rates for specific sales channels and what ad campaigns were associated with these conversions?",
    "How does the revenue generated by a product vary with different advertising strategies across multiple sales channels?",
    "Which promotions had the highest impact on the number of clicks and conversions across various sales channels?",
    "How did different sales channels perform in terms of revenue during a specific marketing campaign?",
    "Which sales channels contributed the most to revenue for specific product groups during a specific ad campaign?",
    "How does the effectiveness of promotions vary across different regions and sales channels?",
    "What is the impact of different ad groups on revenue generated for products within specific categories?",
    "Which customer types (new vs. repeat) are more responsive to specific ad campaigns, and how does this vary across different sales channels?",
    "What is the relationship between the number of conversions and the revenue generated by different products across various sales channels?",
    "Which regions had the highest revenue growth during a specific promotion, and what ad campaigns were associated with this growth?",
    "How does the cost of goods sold (COGS) vary with different advertising strategies across various sales channels?",
    "What is the impact of different customer types on revenue generated during specific promotions across multiple sales channels?",
    "Which ad campaigns generated the most revenue in a specific country, and what were the associated product groups?",
    "How does the number of impressions correlate with revenue growth for different products across multiple sales channels?",
    "Which sales channels had the highest number of conversions during a specific promotion, and what were the associated ad campaigns?",
    "What is the relationship between the number of clicks and the revenue generated by specific products across various sales channels?",
    "Which regions had the highest number of conversions for a specific product group during a specific ad campaign?",
    "How does the number of conversions vary with different ad spend levels across various sales channels?",
    "What is the impact of different product categories on revenue generated during specific ad campaigns across multiple sales channels?",
    "Which ad groups contributed the most to revenue for specific sales channels, and what were the associated promotions?",
    "How does the revenue generated by specific products vary with different customer types across multiple sales channels?",
    "Which regions had the highest revenue growth during a specific ad campaign, and what were the associated product groups?",
    "What is the relationship between ad spend and the number of conversions for specific products across various sales channels?",
    "Which sales channels had the highest revenue growth during a specific promotion, and what were the associated ad campaigns?",
    "How does the revenue generated by specific products vary with different advertising strategies across multiple sales channels?",
    "Which customer types (new vs. repeat) generated the most revenue during a specific ad campaign, and how does this vary across different regions?",
    "What is the impact of different sales channels on revenue generated during specific promotions across multiple regions?",
    "Which ad groups had the highest impact on revenue for specific product groups across various sales channels?",
    "How does the number of impressions correlate with the number of conversions for specific products across multiple sales channels?",
    "Which regions had the highest revenue growth during a specific promotion, and what were the associated ad groups?",
    "What is the impact of different customer types on revenue generated by specific products across multiple sales channels?",
    "Which sales channels had the highest revenue during a specific ad campaign, and what were the associated product groups?",
    "How does the number of conversions vary with different ad spend levels for specific products across various sales channels?",
    "What is the relationship between the number of clicks and the revenue generated by different products across multiple regions?",
    "Which customer types (new vs. repeat) are more responsive to specific ad groups, and how does this vary across different sales channels?",
    "What is the impact of different promotions on the revenue generated by specific products across multiple sales channels?",
    "Which regions had the highest number of conversions for specific ad campaigns, and what were the associated product groups?",
    "How does the revenue generated by specific products vary with different ad campaigns across various sales channels?",
    "Which ad groups had the highest revenue growth during a specific promotion, and what were the associated sales channels?",
    "What is the relationship between ad spend and the revenue generated by specific product categories across various regions?",
    "Which sales channels had the highest number of conversions during a specific ad campaign, and what were the associated promotions?",
    "How does the revenue generated by different products vary with different customer types across multiple sales channels?"

]
# ['Can you help me with yearly sales ?',
#                        'Can we look at sales by year for top 5 categories ?',
#                        'What is 2024 distribution of unique orders in subscribe and save vs all ? Show as pie chart',
#                        'What are the top 8 categories by AOV in 2024?',
#                        # 'Find top 20 Cities by AOV where combined city Sales is greater than $5000 ?',
#                        'Can we do a pareto analysis and find the top 80% sales contributing states?',
#                        'Can we do a pareto analysis and find the top 80% profit contributing states?',
#                        'Which are the top 10 states by margin percentage?',
#                        #    'Can you find top 10 states where total sales > 5,000 and calculate margin ?',
#                        # 'Can you perform RFM analysis and assign segment names?',
#                        # 'Can you show 2023 sales distribution by country as a pie chart?',
#                        'Can you calculate YoY% increase in sales ?',
#                        'Can you calculate QoQ% increase in profit ?',
#                        # 'Can we quantify total loss by subcategory ?',
#                        'Is there any quarterly seasonality in sales across years ?',
#                        'Can we identify any monthly seasonality in sales ?',
#                        'Can you put months on x axis and years on color and make it a line chart',

#                        'What is the trend of customer repeat rate across months ?',

#                        'Which are the top 20 subcategories who give high sales but low profit ?',
#                        # 'Are there any specific states where return rate is high?',
#                        'Is there any correlation between discount, sales and profits ?',
#                        # 'Can you create a scatter plot for profit vs sales at an order level?',
#                        'Can you see if discounts are given in any specific time of the year ?',
#                        'Can you find the top 10 products by profits and track their average discount ?',
#                        # 'Can you analyse the 90 Days Customer lifetime value across categories ?',
#                        # 'Can we analyse 30 days, 60 days and 90 days CLV by Category?',
#                        # 'Can we analyse the 30, 60 90 days CLV by acquisition year ?',
#                        'Help me create a line chart for weekly-yearwise trend of sales?',
#                        'Can you create a line chart of and overlay years on top of each other so week numbers are '
#                        'on x axis and year on color ?',
#                        # 'Can you create a pie chart showing count of orders per ship mode ?',
#                        'Can we create a pie chart breaking down sales by top 10 brands ?'
#                        ]





st.sidebar.write("## Sample Questions")
for i, quest in enumerate(suggested_questions):
    st.sidebar.write(f"{i+1}.  {quest}")
