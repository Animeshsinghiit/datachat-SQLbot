from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ConversationSummaryBufferMemory
from openai import OpenAI


def init_memory(llm, memory_type='window', max_token_limit=2000, k=1):
    if memory_type == 'window':
        return ConversationBufferWindowMemory(llm=llm,
                                            max_token_limit=max_token_limit,
                                            k=k)
    
    elif memory_type  == 'summary':
        return ConversationSummaryBufferMemory(llm=llm,
                                               max_token_limit=max_token_limit,
                                               k=k)


def create_human_readable_response(resp, openai_model='gpt-4o-mini'):
    open_ai_client = OpenAI()
    prompt = f"""
Here's the response from the SQL chain which contains:
- 'user_query': The question asked by the user.
- 'SQL_Query': The SQL query generated for the user's question.
- 'llm_thoughts': Steps taken by the model to arrive at the SQL query for the user's question.
- 'SQL_Result': Result of the SQL query.

Response:
{resp}

Please create a friendly and informative response for the user based on the query and results provided above. Ensure the response clearly addresses the user's question and presents the results in an easy-to-understand and engaging manner.

Guidelines:
- Avoid technical details or references to databases.
- Use simple language and explain the results clearly.
- Structure the response in a well-spaced and visually appealing markdown format.
- Focus on providing a concise summary and actionable insights related to the user's query.
- Do not display the SQL results or include any tables in the response.
- Interpret the results in the context of the user's query, summarizing key points without showing the raw data.
- Do not include any introductory phrases or closing statements.
- Do not present any result or assumption on your own; strictly adhere to the "SQL_Result" field.
- If the "SQL_Result" is empty, simply state that there is no data available, in the most logical and clear way.
- The response should be aimed at management and business users, so focus on providing insights that directly answer their query.

**Markdown Formatting Guidelines:**
- Use **bold** for key points or headers.
- Use bullet points for lists or grouped items.
- Add line breaks between sections to enhance readability.
- Use italics for emphasis when needed.
- Use horizontal lines (`---`) to separate different sections of content for a clean layout.


Final Response (in Markdown format):
    """.strip()
    response = open_ai_client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                     model=openai_model)
    return response.choices[0].message.content

from decimal import Decimal
from datetime import date
import pandas as pd
import json
def convert_sql_result_to_dataframe(sql_result):
    converted_result = []

    sql_result = json.loads(sql_result)
    print(sql_result, type(sql_result))

    for row in sql_result:
        if isinstance(row, dict):
            converted_row = {}
            
            for key, value in row.items():
                if isinstance(value, Decimal):
                    converted_row[key] = float(value)
                elif isinstance(value, date):
                    converted_row[key] = value.isoformat()
                else:
                    converted_row[key] = value
            converted_result.append(converted_row)
        else:
            print(f"Skipping row: {row} because it's not a dictionary")
        # break
        
    return pd.DataFrame(converted_result)

def make_topic_name(first_message, openai_model='gpt-4o-mini'):
    open_ai_client = OpenAI()

    prompt = f""" <Objective>
                Your task is to summarise a user message to a 4-5 word heading. Return only this summary and nothing else.
                This will be used as the heading for the chat that the user does.
                <Objective/>

                <User Message>
                {first_message}
                <User Message/>
                """.strip()
    response = open_ai_client.chat.completions.create(messages=[{"role": "user", "content": prompt}],
                                                     model=openai_model)
    return response.choices[0].message.content