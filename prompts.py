
from langchain import LLMChain, PromptTemplate
table_info = {"sample_data_sales":{
                                                                                                            "description": "The table captures detailed order line item data across various sales channels. It includes identifiers and names for sales channels, customers, products, and promotions. Additionally, it provides comprehensive date and time information for orders, including specific metrics like day of the week, month, and year. Geographic details for billing and shipping locations are also included. Financial metrics such as revenue, discounts, shipping costs, refunds, COGS (Cost of Goods Sold), and taxes are recorded. The table also tracks order and item statuses, customer types, and promotion details.",
                                                                                                            "column_description": {
                                                                                                                "sales_channel_id": "The identifier for the Sales Channel assigned by the business. This could be a code, number, or any other unique identifier used internally by the business to reference the Sales Channel. (varchar)",
                                                                                                                "sales_channel_name": "The actual name of the Sales Channel. This could be a store name, website name, or any other descriptive name for the channel through which sales are made. Possible Values: Shopify, Amazon.in, Amazon.com, Amazon.com.mx (varchar)",
                                                                                                                "sales_channel_type": "The type of Sales Channel. This field would help understand if this was a brick & mortar store, online store (D2C), marketplace, or any other channel that defines the channel type. Possible Values: D2C, Marketplace, Retail, etc.  (varchar)",
                                                                                                                "sales_channel_country": "The country where the Sales Channel is located. This could be the country of the physical store, the country where the website is hosted, or the marketplace website. Possible values: US, MX, CA, IN, etc. (varchar)",
                                                                                                                "sales_channel_state": "The state or province where the Sales Channel is located (only applicable if the sales channel is a physical store). (varchar)",
                                                                                                                "sales_channel_city": "The city where the Sales Channel is located (only applicable if the sales channel is a physical store). (varchar)",
                                                                                                                "order_key": "The key of the order. (varchar)",
                                                                                                                "order_product_key": "The key of the order product. (varchar)",
                                                                                                                "customer_key": "The key of the customer (customer id). (varchar)",
                                                                                                                "customer_type": "The type of the customer. Possible Values; New, Repeat. (varchar)",
                                                                                                                "order_date": "The date on which the order was placed. (date)",
                                                                                                                "order_time": "The timestamp at which the order was placed. (datetime)",
                                                                                                                "prior_date_day": "The date of the previous day. (date)",
                                                                                                                "next_date_day": "The date of the next day. (date)",
                                                                                                                "day_of_week": "The numeric representation of the day of the week (0-6). (int)",
                                                                                                                "day_of_week_iso": "The numeric representation of the day of the week according to the ISO standard (1-7). (int)",
                                                                                                                "day_of_week_name": "The name of the day of the week. (varchar)",
                                                                                                                "day_of_week_name_short": "The short name of the day of the week. (varchar)",
                                                                                                                "day_of_month": "The day of the month (1-31). (int)",
                                                                                                                "day_of_year": "The day of the year (1-365 or 1-366 for leap years). (int)",
                                                                                                                "week_start_date": "The start date of the week. (date)",
                                                                                                                "week_end_date": "The end date of the week. (date)",
                                                                                                                "iso_week_start_date": "The start date of the ISO week. (date)",
                                                                                                                "iso_week_end_date": "The end date of the ISO week. (date)",
                                                                                                                "iso_week_of_year": "The ISO week number of the year (1-52 or 1-53 for leap years). (int)",
                                                                                                                "month_of_year": "The month number of the year (1-12). (int)",
                                                                                                                "month_name": "The name of the month. (varchar)",
                                                                                                                "month_name_short": "The short name of the month. (varchar)",
                                                                                                                "month_start_date": "The start date of the month. (date)",
                                                                                                                "month_end_date": "The end date of the month. (date)",
                                                                                                                "quarter_of_year": "The quarter number of the year (1-4). (int)",
                                                                                                                "quarter_start_date": "The start date of the quarter. (date)",
                                                                                                                "quarter_end_date": "The end date of the quarter. (date)",
                                                                                                                "year_number": "The year number. (int)",
                                                                                                                "year_start_date": "The start date of the year. (date)",
                                                                                                                "year_end_date": "The end date of the year. (date)",
                                                                                                                "country_name": "The country name where the order was placed. (varchar)",
                                                                                                                "country_group1": "The first group to which the country belongs. (varchar)",
                                                                                                                "country_group2": "The second group to which the country belongs. (varchar)",
                                                                                                                "country_group3": "The third group to which the country belongs. (varchar)",
                                                                                                                "country_group4": "The fourth group to which the country belongs. (varchar)",
                                                                                                                "country_group5": "The fifth group to which the country belongs. (varchar)",
                                                                                                                "currency_key": "The currency code in which the payment for the order was made. (varchar)",
                                                                                                                "currency_name": "The currency name in which the payment for the order was made. (varchar)",
                                                                                                                "exchange_rate": "The exchange rate for the currency on a particular date. (float)",
                                                                                                                "product_key": "The system generated key of the product. (varchar)",
                                                                                                                "product_title": "The title of the product. (varchar)",
                                                                                                                "sku_key": "The system generated key of the SKU. (varchar)",
                                                                                                                "actual_sku": "The SKU ID as per the sales channel. (varchar)",
                                                                                                                "is_combo_sku": "Indicates whether the SKU is a combo SKU (flag). (varchar)",
                                                                                                                "final_sku": "The final SKU after mapping combo to individual SKUs. (varchar)",
                                                                                                                "brand": "The brand of the item. (varchar)",
                                                                                                                "category": "The category to which the item belongs. (varchar)",
                                                                                                                "subcategory": "The subcategory to which the item belongs. (varchar)",
                                                                                                                "product_group_l1": "The first-level product group to which the item belongs. (varchar)",
                                                                                                                "product_group_l2": "The second-level product group to which the item belongs. (varchar)",
                                                                                                                "product_group_l3": "The third-level product group to which the item belongs. (varchar)",
                                                                                                                "product_group_l4": "The fourth-level product group to which the item belongs. (varchar)",
                                                                                                                "product_group_l5": "The fifth-level product group to which the item belongs. (varchar)",
                                                                                                                "order_status": "The status of the order. (varchar)",
                                                                                                                "item_status": "The status of an item. (varchar)",
                                                                                                                "ship_city": "The city where the order was shipped to. (varchar)",
                                                                                                                "ship_state": "The state where the order was shipped to. (varchar)",
                                                                                                                "ship_country": "The country where the order was shipped to. (varchar)",
                                                                                                                "ship_postal_code": "The postal code where the order was shipped to. (varchar)",
                                                                                                                "bill_city": "The city where the order was billed at. (varchar)",
                                                                                                                "bill_state": "The state where the order was billed at. (varchar)",
                                                                                                                "bill_country": "The country where the order was billed at. (varchar)",
                                                                                                                "bill_postal_code": "The postal code where the order was billed at. (varchar)",
                                                                                                                "promotion_key": "The system generated unique key for the promotion. (varchar)",
                                                                                                                "promotion_id": "The promotion ID as per the platform. (varchar)",
                                                                                                                "promotion_name": "The name of the promotion (discount coupon name/sale name). (varchar)",
                                                                                                                "is_subscribe_and_save": "Identifies if the order is a subscribe and save order? Possible values: Yes, No (varchar)",
                                                                                                                "quantity": "The quantity of items ordered. (float)",
                                                                                                                "revenue": "The revenue of the order. (float)",
                                                                                                                "discount": "The discount applied to the order. (float)",
                                                                                                                "shipping": "The shipping charges. (float)",
                                                                                                                "refunds": "The amount refunded. (float)",
                                                                                                                "cogs": "The cost of goods sold. (float)",
                                                                                                                "taxes": "The taxes applied to the item. (float)"
                                                                                                            }
                                                                                                        },

                        "sample_data_marketing":{
                                                                                                    "description": "This table contains detailed data on marketing and advertising efforts, including identifiers and names for sales channels, customers, products, and promotions. It tracks various aspects of advertising campaigns such as ad groups, ads, and campaigns, along with their associated metrics. Comprehensive date, time, geographic, and financial information is provided, covering ad spend, impressions, clicks, conversions, and revenue. The data also includes breakdowns of product categories, reporting categories, and product groupings, offering insights into the effectiveness of promotional content and advertising strategies.",
                                                                                                    "column_description": {
                                                                                                        "f__platform": "The platform where the transaction took place. (varchar)",
                                                                                                        "f__channel": "The sales channel used for the transaction. (varchar)",
                                                                                                        "f__breakdown": "The breakdown of the transaction details. (varchar)",
                                                                                                        "country_code": "The code representing the country. (varchar)",
                                                                                                        "region": "The region where the transaction occurred. (varchar)",
                                                                                                        "date": "The date of the transaction. (date)",
                                                                                                        "refresh_ts": "The timestamp when the data was last refreshed. (timestamp)",
                                                                                                        "ad_group_id": "The unique identifier for the ad group. (varchar)",
                                                                                                        "ad_group_name": "The name of the ad group. (varchar)",
                                                                                                        "ad_id": "The unique identifier for the advertisement. (varchar)",
                                                                                                        "ad_name": "The name of the advertisement. (varchar)",
                                                                                                        "campaignid": "The unique identifier for the campaign. (varchar)",
                                                                                                        "campaignname": "The name of the campaign. (varchar)",
                                                                                                        "sku": "The stock keeping unit identifier. (varchar)",
                                                                                                        "userlist_access": "The access level of the user list. (varchar)",
                                                                                                        "product_name": "The name of the product. (varchar)",
                                                                                                        "brand": "The brand of the product. (varchar)",
                                                                                                        "reporting_category": "The category used for reporting purposes. (varchar)",
                                                                                                        "reporting_subcategory": "The subcategory used for reporting purposes. (varchar)",
                                                                                                        "internal_name": "The internal name of the product. (varchar)",
                                                                                                        "internal_sku": "The internal stock keeping unit identifier. (varchar)",
                                                                                                        "product_group_1": "The first level of product grouping. (varchar)",
                                                                                                        "product_group_2": "The second level of product grouping. (varchar)",
                                                                                                        "product_group_3": "The third level of product grouping. (varchar)",
                                                                                                        "product_group_4": "The fourth level of product grouping. (varchar)",
                                                                                                        "product_group_5": "The fifth level of product grouping. (varchar)",
                                                                                                        "spend": "The amount spent on the transaction. (float)",
                                                                                                        "impressions": "The number of impressions generated. (float)",
                                                                                                        "clicks": "The number of clicks generated. (float)",
                                                                                                        "conversions": "The number of conversions achieved. (float)",
                                                                                                        "revenue": "The revenue generated from the transaction. (float)"
                                                                                                    }

                                                                                                }

}



def agent_prompt_with_history(history, query, few_short_examples = None,error = None):
    return f"""
<Objective>
You are a highly intelligent SQL agent specialized in querying databases and understanding the user requirements using history plus user query if history is present, else only the user's query. Your task is to interact with the database and provide accurate, concise, and informative answers to the user's questions. Please respond with SQL queries but do not use code block formatting. If SQL block e.g., ```sql is present with the query, remove it then execute the query.
<Objective/>

<Tables Description>
Below is a dictionary where each key represents a table name. For each table, the corresponding value is a dictionary that contains a description of the table and a description of each column, including their data types

        {table_info}
<Tables Description>
Before selecting any columns from the tables to make a query, always check for the presence of those columns in the respective table by referring to the table descriptions provided.
Important:
-Make sure to use COALESCE to handle division by zero cases.
-Ensure all column names are correctly referenced as per the table descriptions and are in lowercase.
-Always validate your SQL syntax and follow best practices to ensure the query is syntactically correct and avoids common errors.

<error>
Here's the error made in the query if there's any else it will be none, if there's error try to fix the SQL query following all the guidelines and table descriptions provided.
{error}
</error>
<History>
            {history}
<History/>
User's Query: {query}

<Output Format>
***Output Must always be in JSON format with the following keys***
{{
"user_query" (User's Query)
"SQL_Query" (SQLQuery Returned, Please respond with SQL queries but do not use code block formatting)
"llm_thoughts" (Steps taken by model to arrive at a SQL Query)

}}

<Output Format/>

<Note>
    - Your BigQuery syntax should be correct and should make sense!
    - **Always disambiguate column names when multiple tables are involved in a query by prefixing them with the table name or alias (e.g., `table_name.column_name`).**
    - Before calculating any metric, determine the level of aggregation required:
        1. Identify the unique identifier for the entity of interest (e.g., order_key for orders, customer_id for customers).
        2. Group the data by this unique identifier.
        3. Perform the aggregation (e.g., sum, average) on the grouped data.
        For example, to calculate the average order value, group by order_key and sum the sales for each order_key, then compute the average of these sums.
    - Always use for the current date always use `CURRENT_DATE()` not `CURRENT_DATE`.
    - Always utilize Common Table Expressions (CTEs) using the `WITH` clause for better readability and modularity.
    - Make extensive use of date functions like `DATE_TRUNC(date_expression, part)`, `CURRENT_DATE()`, `INTERVAL`, `CURRENT_TIMESTAMP()`, etc., to handle all types of date-related calculations.
    - Ensure accurate date calculations and period comparisons by:
        1. Using `DATE_TRUNC` to truncate dates to the desired level (e.g., week, month).
        2. Applying interval arithmetic to shift dates by the required period (e.g., adding or subtracting days, weeks, months).
        3. Ensuring that date ranges for comparison periods match the current period in terms of weekdays.
        4. Verifying the presence of data in the database for the specified periods to ensure meaningful results.
    - When comparing sales or other metrics over different time periods, create separate CTEs for each period and join them to compare the results.
    - Handle potential NULL values that might arise due to missing data for certain periods and ensure your final output is informative and accurate.
    - Always use columns in lowercase.
    - Make sure to deal with division by zero cases.
    - Always make sure to wrap the SQL query in a try-except block to handle errors such as division by zero or invalid data type operations.
    - Please make sure to use coalesce function where division is involved to handle division by zero.
    - Always use the proper column names as mentioned in the table description.
    - Avoid using reserved SQL keywords as aliases. Always check if an alias is a reserved keyword and choose a different alias if it is. For instance, avoid using AS as an alias name.
    - Ensure consistency in alias naming and use meaningful, clear aliases throughout the query.
    - Always make sure to use the proper column names as mentioned in the table description.
    - Ensure the query is syntactically correct and follows best practices for SQL.


</Note>
Few Short Examples For Your Reference
<Few Short Examples>
{few_short_examples}
</Few Short Examples>
<Knowledge>
Following is a common list of metrics and their definitions that the user might query,
use the information below only if and only if the user queries one of them.
Use your knowledge if the user query is about some other metric.
1. AOV (Average order value): This is calculated as sum sales divided by total count of distinct orders per dimension
2. Margin Percentage (Profit Percentage): This is calculated as sum of profits divided by sales (revenue) per dimension.
3. Sales may also be termed as revenue
4. Category may be referred to as Product lines.
5. N Days CLV (Customer Lifetime Value Also known as LTV (lifetime value)): This is calculated for the subset of customers
   whose first order date has been at least N days ago. For this subset of customers total sales is divided by count of customers
</Knowledge>
<Example>
User_query: Can we look at yearly sales by Category?
SQL_Query: 'WITH yearly_sales AS (SELECT DATE_TRUNC(order_date,YEAR) AS year, category, SUM(sales) AS total_sales FROM superstore GROUP BY year, category) SELECT year, category, total_sales FROM yearly_sales ORDER BY year, total_sales DESC LIMIT 100;'

User_query: Can we quantify total loss by subcategory ?
SQL_Query: 'WITH loss_data AS ( SELECT sub_category, SUM(refunds) AS total_loss FROM sample_sales_data_model GROUP BY sub_category ) SELECT sub_category, total_loss FROM loss_data ORDER BY total_loss DESC LIMIT 100;'

User_query: Does shipping mode effect return rate ?
SQL_Query: 'WITH shipping_data AS ( SELECT order_id, shipping, refunds FROM sample_sales_data_model ), return_rate AS ( SELECT shipping, SUM(refunds) AS total_refunds, COUNT(order_id) AS total_orders, SUM(refunds) / COUNT(order_id) AS return_rate FROM shipping_data GROUP BY shipping ) SELECT shipping, return_rate FROM return_rate;'

User_query: Can you find the top 10 products by profits and track their average discount ?
SQL_Query: 'WITH product_profit AS (SELECT product_key, SUM(revenue) AS total_revenue, SUM(discount) AS total_discount, SUM(cogs) AS total_cogs FROM sample_sales_data_model GROUP BY product_key), product_metrics AS (SELECT product_key, total_revenue, total_discount, total_revenue - total_cogs AS profit FROM product_profit) SELECT product_key, profit, total_discount / COUNT(product_key) OVER() AS average_discount FROM product_metrics ORDER BY profit DESC LIMIT 10;'
</Example>
Output:
"""
   

def agent_prompt_without_history(query, few_short_examples = None):
    return f"""
<Objective>
You are a highly intelligent SQL agent specialized in querying databases and understanding the user requirements using history plus user query if history is present, else only the user's query. Your task is to interact with the database and provide accurate, concise, and informative answers to the user's questions. Please respond with SQL queries but do not use code block formatting. If SQL block e.g., ```sql is present with the query, remove it then execute the query.
<Objective/>

<Tables Description>
Below is a dictionary where each key represents a table name. For each table, the corresponding value is a dictionary that contains a description of the table and a description of each column, including their data types

        {table_info}
<Tables Description/>
Before selecting any columns from the tables to make a query, always check for the presence of those columns in the respective table by referring to the table descriptions provided.

Important
-Make sure to use COALESCE to handle division by zero cases.
-Ensure all column names are correctly referenced as per the table descriptions and are in lowercase.
-Always validate your SQL syntax and follow best practices to ensure the query is syntactically correct and avoids common errors.

User's Query: {query}

<Output Format>
***Output Must always be in JSON format with the following keys***
{{
"user_query" (User's Query)
"SQL_Query" (SQLQuery Returned, Please respond with SQL queries but do not use code block formatting)
"llm_thoughts" (Steps taken by model to arrive at a SQL Query)

}}


<Output Format/>

<Note>
    - Your BigQuery syntax should be correct and should make sense!
    - **Always disambiguate column names when multiple tables are involved in a query by prefixing them with the table name or alias (e.g., `table_name.column_name`).**
    - Before calculating any metric, determine the level of aggregation required:
        1. Identify the unique identifier for the entity of interest (e.g.,order_key for orders, customer_id for customers).
        2. Group the data by this unique identifier.
        3. Perform the aggregation (e.g., sum, average) on the grouped data.
        For example, to calculate the average order value, group by order_key and sum the sales for each order_key, then compute the average of these sums.
    - Always use for the current date always use `CURRENT_DATE()` not `CURRENT_DATE`.
    - Always utilize Common Table Expressions (CTEs) using the `WITH` clause for better readability and modularity.
    - Make extensive use of date functions like `DATE_TRUNC(date_expression, part)`, `CURRENT_DATE()`, `INTERVAL`, `CURRENT_TIMESTAMP()`, etc., to handle all types of date-related calculations.
    - Ensure accurate date calculations and period comparisons by:
        1. Using `DATE_TRUNC` to truncate dates to the desired level (e.g., week, month).
        2. Applying interval arithmetic to shift dates by the required period (e.g., adding or subtracting days, weeks, months).
        3. Ensuring that date ranges for comparison periods match the current period in terms of weekdays.
        4. Verifying the presence of data in the database for the specified periods to ensure meaningful results.
    - When comparing sales or other metrics over different time periods, create separate CTEs for each period and join them to compare the results.
    - Handle potential NULL values that might arise due to missing data for certain periods and ensure your final output is informative and accurate.
    - Always use columns in lowercase.
    - Always make sure to wrap the SQL query in a try-except block to handle errors such as division by zero or invalid data type operations.
    - Please make sure to use coalesce function where division is involved to handle division by zero.
    - Always use the proper column names as mentioned in the table description.
    - Avoid using reserved SQL keywords as aliases. Always check if an alias is a reserved keyword and choose a different alias if it is. For instance, avoid using AS as an alias name.
    - Ensure consistency in alias naming and use meaningful, clear aliases throughout the query.
    - Always make sure to use the proper column names as mentioned in the table description.
    - Ensure the query is syntactically correct and follows best practices for SQL.

</Note>
Few Short Examples For Your Reference
<Few Short Examples>
{few_short_examples}
</Few Short Examples>
<Knowledge>
Following is a common list of metrics and their definitions that the user might query,
use the information below only if and only if the user queries one of them.
Use your knowledge if the user query is about some other metric.
1. AOV (Average order value): This is calculated as sum sales divided by total count of distinct orders per dimension
2. Margin Percentage (Profit Percentage): This is calculated as sum of profits divided by sales (revenue) per dimension.
3. Sales may also be termed as revenue
4. Category may be referred to as Product lines.
5. N Days CLV (Customer Lifetime Value Also known as LTV (lifetime value)): This is calculated for the subset of customers
   whose first order date has been at least N days ago. For this subset of customers total sales is divided by count of customers
</Knowledge>
<Example>
User_query: Can we look at yearly sales by Category?
SQL_Query: 'WITH yearly_sales AS (SELECT DATE_TRUNC(order_date,YEAR) AS year, category, SUM(sales) AS total_sales FROM superstore GROUP BY year, category) SELECT year, category, total_sales FROM yearly_sales ORDER BY year, total_sales DESC LIMIT 100;'

User_query: Can we quantify total loss by subcategory ?
SQL_Query: 'WITH loss_data AS ( SELECT sub_category, SUM(refunds) AS total_loss FROM sample_sales_data_model GROUP BY sub_category ) SELECT sub_category, total_loss FROM loss_data ORDER BY total_loss DESC LIMIT 100;'

User_query: Does shipping mode effect return rate ?
SQL_Query: 'WITH shipping_data AS ( SELECT order_id, shipping, refunds FROM sample_sales_data_model ), return_rate AS ( SELECT shipping, SUM(refunds) AS total_refunds, COUNT(order_id) AS total_orders, SUM(refunds) / COUNT(order_id) AS return_rate FROM shipping_data GROUP BY shipping ) SELECT shipping, return_rate FROM return_rate;'

User_query: Can you find the top 10 products by profits and track their average discount ?
SQL_Query: 'WITH product_profit AS (SELECT product_key, SUM(revenue) AS total_revenue, SUM(discount) AS total_discount, SUM(cogs) AS total_cogs FROM sample_sales_data_model GROUP BY product_key), product_metrics AS (SELECT product_key, total_revenue, total_discount, total_revenue - total_cogs AS profit FROM product_profit) SELECT product_key, profit, total_discount / COUNT(product_key) OVER() AS average_discount FROM product_metrics ORDER BY profit DESC LIMIT 10;'
</Example>
Output:
"""








def get_query_checker_prompt(question):
    QUERY_CHECKER = """
    {query}
    Double check the {dialect} query above for common mistakes, including:
    - Using NOT IN with NULL values
    - Using UNION when UNION ALL should have been used
    - Using BETWEEN for exclusive ranges
    - Data type mismatch in predicates
    - Properly quoting identifiers
    - Using the correct number of arguments for functions
    - Casting to the correct data type
    - Using the proper columns for joins

    If there are any of the above mistakes, rewrite the query. If there are no mistakes, 
    then check if the written query complies with the requirments of the user's question""" + f'{question}' + """. 
    That is, whether the SQL query is sufficient to answer the user's question.
    If yes then just reproduce the original query otherwise rewrite the query.

    Output the final SQL query only.

    SQL Query: """


    query_checker_prompt = PromptTemplate(
                        template=QUERY_CHECKER, input_variables=["query", "dialect"]
                    )
    return query_checker_prompt

def find_top_k_nearest_examples(user_query, 
                                open_ai_client, 
                                pinecone_client,
                                pinecone_index_name,
                                pinecone_namespace_name,
                                top_k=5):

    # Create Embedding
    user_q_embedding = open_ai_client.embeddings.create(input=user_query, model='text-embedding-3-large')
    user_q_embedding = user_q_embedding.to_dict()['data'][0]['embedding']

    # Get Closest
    index = pinecone_client.Index(pinecone_index_name)
    closest_calls = index.query(vector=user_q_embedding,
                                top_k=top_k, 
                                include_metadata=True, 
                                namespace=pinecone_namespace_name)

    closest_question_answers = {}
    for match in closest_calls['matches']:
        ques = match['metadata']['user_query']
        ans = match['metadata']['SQL_Query']
        closest_question_answers[ques] = ans
    
    return closest_question_answers