fine_tune_data = [
    {
        "question": "What is the total revenue generated from each sales channel in the last quarter?",
        "answer": "WITH last_quarter AS (SELECT sales_channel_name, SUM(revenue) AS total_revenue FROM sample_sales_data_model WHERE order_date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 QUARTER), QUARTER) AND order_date < DATE_TRUNC(CURRENT_DATE(), QUARTER) GROUP BY sales_channel_name) SELECT sales_channel_name, total_revenue FROM last_quarter ORDER BY total_revenue DESC;"

     },
     {
        "question": "How does the revenue from new customers compare to repeat customers for the past year?",
        "answer": "WITH customer_revenue AS (SELECT customer_type, SUM(revenue) AS total_revenue FROM sample_sales_data_model WHERE order_date >= DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR), YEAR) GROUP BY customer_type) SELECT customer_type, total_revenue FROM customer_revenue;"

     },
     {
        "question": "What is the average order value for each sales channel?",
        "answer": "WITH order_values AS (SELECT sales_channel_name, SUM(revenue) AS total_revenue, COUNT(DISTINCT order_product_key) AS total_orders FROM sample_sales_data_model GROUP BY sales_channel_name) SELECT sales_channel_name, total_revenue / NULLIF(total_orders, 0) AS average_order_value FROM order_values;"

     },
     {
        "question": "How many new customers were acquired through each sales channel in the last quarter?",
        "answer": "WITH new_customers AS (SELECT sales_channel_name, COUNT(DISTINCT customer_key) AS new_customers_count FROM sample_sales_data_model WHERE customer_type = 'New' AND order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) GROUP BY sales_channel_name) SELECT sales_channel_name, new_customers_count FROM new_customers ORDER BY new_customers_count DESC;"

     },
     {
         "question": "Which sales channels are performing best in terms of revenue across different platforms?",
        "answer": "WITH revenue_data AS (SELECT sales_channel_name, SUM(revenue) AS total_revenue FROM sample_data_sales GROUP BY sales_channel_name) SELECT sales_channel_name, total_revenue FROM revenue_data ORDER BY total_revenue DESC LIMIT 100;"
     },
     {
         "question": "What is the relationship between the advertising spend and revenue generated for each product category?",
        "answer": "WITH category_performance AS (SELECT reporting_category, SUM(spend) AS total_spend, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY reporting_category) SELECT reporting_category, total_spend, total_revenue FROM category_performance ORDER BY total_revenue DESC LIMIT 100;"
     },
     {
         "question": "How do conversion rates vary by country for different marketing campaigns?",
        "answer": "WITH campaign_data AS (SELECT country_code, campaignname, SUM(conversions) AS total_conversions, SUM(impressions) AS total_impressions FROM sample_data_marketing GROUP BY country_code, campaignname) SELECT country_code, campaignname, total_conversions, total_impressions, COALESCE(total_conversions / NULLIF(total_impressions, 0), 0) AS conversion_rate FROM campaign_data ORDER BY conversion_rate DESC LIMIT 100;"
     },
     {
         "question": "What are the most popular products based on sales and impressions in various regions?",
        "answer": "WITH sales_data AS (SELECT product_name, SUM(revenue) AS total_sales, SUM(impressions) AS total_impressions FROM sample_data_marketing GROUP BY product_name), impressions_data AS (SELECT product_name, SUM(impressions) AS total_impressions FROM sample_data_marketing GROUP BY product_name) SELECT s.product_name, s.total_sales, i.total_impressions FROM sales_data s JOIN impressions_data i ON s.product_name = i.product_name ORDER BY s.total_sales DESC, i.total_impressions DESC LIMIT 100;"

     },
     {
         "question": "How does the discount applied to orders correlate with the marketing spend for each advertising campaign?",
        "answer": "WITH order_discount AS (SELECT order_key, SUM(discount) AS total_discount FROM sample_data_sales GROUP BY order_key), marketing_spend AS (SELECT campaignid, SUM(spend) AS total_spend FROM sample_data_marketing GROUP BY campaignid) SELECT md.campaignid, md.total_spend, od.total_discount FROM marketing_spend md LEFT JOIN order_discount od ON md.campaignid = od.order_key LIMIT 100;"
        
     }
     ,{
         "question": "Which product groups have the highest revenue and spend across different ad groups?",
        "answer": "WITH product_group_metrics AS (SELECT product_group_1, SUM(revenue) AS total_revenue, SUM(spend) AS total_spend FROM sample_data_marketing GROUP BY product_group_1) SELECT product_group_1, total_revenue, total_spend FROM product_group_metrics ORDER BY total_revenue DESC, total_spend DESC LIMIT 100;"
        
     }
     ,{
         "question": "What are the average impressions and clicks for each product group in different sales channels?",
        "answer": "WITH impressions_clicks AS (SELECT f__platform, f__channel, product_group_1, AVG(impressions) AS avg_impressions, AVG(clicks) AS avg_clicks FROM sample_data_marketing GROUP BY f__platform, f__channel, product_group_1) SELECT f__platform, f__channel, product_group_1, avg_impressions, avg_clicks FROM impressions_clicks ORDER BY avg_impressions DESC LIMIT 100;"
        
     }
     ,{
         "question": "How do the revenues for different product brands compare to their advertising spend?",
        "answer": "WITH brand_revenue AS (SELECT brand, SUM(revenue) AS total_revenue FROM sample_data_sales GROUP BY brand), brand_spend AS (SELECT brand, SUM(spend) AS total_spend FROM sample_data_marketing GROUP BY brand) SELECT a.brand, a.total_revenue, b.total_spend FROM brand_revenue a JOIN brand_spend b ON a.brand = b.brand ORDER BY a.total_revenue DESC LIMIT 100;"
        
     }
     ,{
         "question": "What are the trends in sales and advertising spend over time for specific marketing campaigns?",
        "answer": "WITH sales_data AS (SELECT DATE_TRUNC(order_date, MONTH) AS month, SUM(revenue) AS total_sales FROM sample_data_sales GROUP BY month), marketing_data AS (SELECT DATE_TRUNC(date, MONTH) AS month, SUM(spend) AS total_spend FROM sample_data_marketing GROUP BY month) SELECT s.month, s.total_sales, m.total_spend FROM sales_data s JOIN marketing_data m ON s.month = m.month ORDER BY s.month LIMIT 100;"
        
     }
     ,{
         "question": "Which customer segments show the highest response rates to specific marketing campaigns?",
        "answer": "WITH marketing_data AS (SELECT ad_group_name, SUM(clicks) AS total_clicks, SUM(conversions) AS total_conversions FROM sample_data_marketing GROUP BY ad_group_name), response_rates AS (SELECT ad_group_name, total_clicks, total_conversions, COALESCE(total_conversions / NULLIF(total_clicks, 0), 0) AS response_rate FROM marketing_data) SELECT ad_group_name, response_rate FROM response_rates ORDER BY response_rate DESC LIMIT 100;"
        
     }
     ,{
         "question": "What is the correlation between the number of impressions and the number of items sold for different product categories?",
        "answer": "WITH impressions_data AS (SELECT product_group_1, SUM(impressions) AS total_impressions FROM sample_data_marketing GROUP BY product_group_1), sales_data AS (SELECT product_group_l1, SUM(quantity) AS total_quantity FROM sample_data_sales GROUP BY product_group_l1) SELECT i.product_group_1, i.total_impressions, s.total_quantity FROM impressions_data i JOIN sales_data s ON i.product_group_1 = s.product_group_l1 LIMIT 100;"        
     }
     ,{
         "question": "Which promotions are most effective in driving sales through specific sales channels?",
        "answer": "WITH promotion_sales AS (SELECT promotion_name, sales_channel_name, SUM(revenue) AS total_revenue FROM sample_data_sales WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY promotion_name, sales_channel_name) SELECT promotion_name, sales_channel_name, total_revenue FROM promotion_sales ORDER BY total_revenue DESC LIMIT 100;"        
     }
     ,{
         "question": "How do order statuses vary across different advertising campaigns and sales channels?",
        "answer": "WITH campaign_data AS (SELECT campaignname, sales_channel_name, order_status, COUNT(order_key) AS order_count FROM sample_data_sales JOIN sample_data_marketing ON sample_data_sales.order_product_key = sample_data_marketing.sku GROUP BY campaignname, sales_channel_name, order_status) SELECT campaignname, sales_channel_name, order_status, order_count FROM campaign_data ORDER BY order_count DESC LIMIT 100;"        
     }
     ,{
         "question": "Which geographic regions generate the highest revenue for specific marketing campaigns?",
        "answer": "WITH campaign_revenue AS (SELECT region, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY region) SELECT region, total_revenue FROM campaign_revenue ORDER BY total_revenue DESC LIMIT 100;"        
     }
     ,{
         "question": "Which products have the highest return rates and how do they correlate with the marketing spend?",
        "answer": "WITH return_data AS (SELECT actual_sku, SUM(refunds) AS total_refunds, COUNT(order_key) AS total_orders, SUM(refunds) / NULLIF(COUNT(order_key), 0) AS return_rate FROM sample_data_sales GROUP BY actual_sku), marketing_data AS (SELECT sku, SUM(spend) AS total_spend FROM sample_data_marketing GROUP BY sku) SELECT r.actual_sku, r.return_rate, m.total_spend FROM return_data r JOIN marketing_data m ON r.actual_sku = m.sku ORDER BY r.return_rate DESC LIMIT 100;"        
     }
       ,{
         "question": "What is the impact of different advertising campaigns on sales across various countries?",
        "answer": "WITH campaign_sales AS (SELECT m.campaignname, s.country_name, SUM(s.revenue) AS total_revenue FROM sample_data_marketing m JOIN sample_data_sales s ON m.sku = s.actual_sku GROUP BY m.campaignname, s.country_name) SELECT campaignname, country_name, total_revenue FROM campaign_sales ORDER BY total_revenue DESC LIMIT 100;"        
     }
      ,{
         "question": "How do shipping costs impact the effectiveness of different ad groups in generating revenue?",
        "answer": "WITH shipping_data AS (SELECT order_product_key, SUM(shipping) AS total_shipping FROM sample_data_sales GROUP BY order_product_key), revenue_data AS (SELECT ad_group_id, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY ad_group_id) SELECT s.order_product_key, s.total_shipping, r.total_revenue FROM shipping_data s JOIN revenue_data r ON s.order_product_key = r.ad_group_id ORDER BY r.total_revenue DESC LIMIT 100;"        
     }
      ,{
         "question": "What is the average order value for each sales channel and how does it relate to the ad spend?",
        "answer": "WITH order_values AS (SELECT sales_channel_name, SUM(revenue) AS total_revenue, COUNT(DISTINCT order_key) AS total_orders FROM sample_data_sales GROUP BY sales_channel_name), average_order_value AS (SELECT sales_channel_name, total_revenue / NULLIF(total_orders, 0) AS average_order_value FROM order_values), ad_spend AS (SELECT f__channel, SUM(spend) AS total_ad_spend FROM sample_data_marketing GROUP BY f__channel) SELECT aov.sales_channel_name, aov.average_order_value, COALESCE(ad.total_ad_spend, 0) AS total_ad_spend FROM average_order_value aov LEFT JOIN ad_spend ad ON aov.sales_channel_name = ad.f__channel LIMIT 100;"        
     }
      ,{
         "question": "How does the time of day impact the success of marketing campaigns in terms of sales and clicks?",
        "answer": "WITH campaign_data AS (SELECT DATE(refresh_ts) AS order_date, SUM(clicks) AS total_clicks, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY order_date) SELECT order_date, total_clicks, total_revenue FROM campaign_data ORDER BY order_date DESC LIMIT 100;"        
     }
      ,{
         "question": "What is the relationship between customer types (new vs. repeat) and their response to marketing campaigns?",
        "answer": "WITH marketing_data AS (SELECT customer_type, SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks, SUM(conversions) AS total_conversions FROM sample_data_marketing JOIN sample_data_sales ON sample_data_marketing.ad_id = sample_data_sales.order_product_key GROUP BY customer_type) SELECT customer_type, total_impressions, total_clicks, total_conversions, COALESCE(total_clicks / NULLIF(total_impressions, 0), 0) AS click_through_rate, COALESCE(total_conversions / NULLIF(total_clicks, 0), 0) AS conversion_rate FROM marketing_data;"        
     }
     ,{
         "question": "What is the total revenue generated by specific sales channels for products that were part of a particular ad campaign?",
        "answer": "WITH campaign_revenue AS (SELECT s.sales_channel_name, SUM(s.revenue) AS total_revenue FROM sample_data_sales s JOIN sample_data_marketing m ON s.order_product_key = m.sku WHERE m.campaignid = 'specific_campaign_id' GROUP BY s.sales_channel_name) SELECT sales_channel_name, total_revenue FROM campaign_revenue ORDER BY total_revenue DESC LIMIT 100;"        
     }
    ,{
         "question": "Which sales channels had the highest conversion rates during promotions and how does this compare across different countries?",
        "answer": "WITH promotion_data AS (SELECT f__channel AS sales_channel_name, country_code AS country_name, SUM(conversions) AS total_conversions, SUM(impressions) AS total_impressions FROM sample_data_marketing WHERE userlist_access IS NOT NULL GROUP BY f__channel, country_code), conversion_rates AS (SELECT sales_channel_name, country_name, COALESCE(SUM(total_conversions) / NULLIF(SUM(total_impressions), 0), 0) AS conversion_rate FROM promotion_data GROUP BY sales_channel_name, country_name) SELECT sales_channel_name, country_name, conversion_rate FROM conversion_rates ORDER BY conversion_rate DESC LIMIT 100;"        
     }
   ,{
         "question": "How does the average discount offered in a specific ad group correlate with the increase in product revenue across different sales channels?",
        "answer": "WITH ad_group_discount AS (SELECT ad_group_name, AVG(spend) AS average_discount FROM sample_data_marketing GROUP BY ad_group_name), revenue_data AS (SELECT f__channel, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY f__channel) SELECT ad_group_discount.ad_group_name, ad_group_discount.average_discount, revenue_data.total_revenue FROM ad_group_discount JOIN revenue_data ON ad_group_discount.ad_group_name = revenue_data.f__channel;"        
     }
   ,{
         "question": "What is the impact of ad spend on the revenue of new versus repeat customers across various sales channels?",
        "answer": "WITH ad_spend_revenue AS (SELECT s.customer_type, SUM(m.spend) AS total_ad_spend, SUM(s.revenue) AS total_revenue FROM sample_data_marketing m JOIN sample_data_sales s ON m.sku = s.actual_sku GROUP BY s.customer_type) SELECT customer_type, total_ad_spend, total_revenue FROM ad_spend_revenue;"        
     }
     ,{
         "question": "Which product categories saw the highest revenue growth during a specific ad campaign, and what were the associated promotion details?",
        "answer": "WITH campaign_revenue AS (SELECT campaignname, product_group_1, SUM(revenue) AS total_revenue FROM sample_data_marketing WHERE campaignname IS NOT NULL GROUP BY campaignname, product_group_1), revenue_growth AS (SELECT campaignname, product_group_1, total_revenue, LAG(total_revenue) OVER (PARTITION BY product_group_1 ORDER BY campaignname) AS previous_revenue FROM campaign_revenue) SELECT campaignname, product_group_1, total_revenue, previous_revenue, (total_revenue - COALESCE(previous_revenue, 0)) AS revenue_growth FROM revenue_growth WHERE previous_revenue IS NOT NULL ORDER BY revenue_growth DESC LIMIT 100;"        
     }
     ,{
         "question": "What is the correlation between the number of impressions and the final revenue across different regions for specific products?",
        "answer": "WITH impressions_revenue AS (SELECT region, SUM(impressions) AS total_impressions, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY region) SELECT region, total_impressions, total_revenue FROM impressions_revenue ORDER BY total_revenue DESC LIMIT 100;"        
     }
     ,{
         "question": "How did different customer types (new vs. repeat) respond to various ad campaigns in terms of revenue generated?",
        "answer": "WITH ad_campaign_revenue AS (SELECT marketing.f__channel, sales.customer_type, SUM(sales.revenue) AS total_revenue FROM sample_data_marketing AS marketing JOIN sample_data_sales AS sales ON marketing.sku = sales.actual_sku GROUP BY marketing.f__channel, sales.customer_type) SELECT f__channel, customer_type, total_revenue FROM ad_campaign_revenue ORDER BY total_revenue DESC LIMIT 100;" 

     }
     ,{
         "question": "What is the relationship between ad spend and average order value across different sales channels?",
        "answer": "WITH order_values AS (SELECT order_key, SUM(revenue) AS total_revenue FROM sample_data_sales GROUP BY order_key), average_order_value AS (SELECT AVG(total_revenue) AS aov FROM order_values), ad_spend AS (SELECT SUM(spend) AS total_spend FROM sample_data_marketing) SELECT (SELECT aov FROM average_order_value) AS average_order_value, (SELECT total_spend FROM ad_spend) AS total_ad_spend;" 
               
     }
     ,{
         "question": "Which geographic regions saw the highest conversion rates for specific sales channels and what ad campaigns were associated with these conversions?",
        "answer": "WITH conversion_data AS (SELECT f__channel, region, SUM(conversions) AS total_conversions, SUM(impressions) AS total_impressions FROM sample_data_marketing GROUP BY f__channel, region), conversion_rates AS (SELECT f__channel, region, COALESCE(SUM(total_conversions) / NULLIF(SUM(total_impressions), 0), 0) AS conversion_rate FROM conversion_data GROUP BY f__channel, region) SELECT f__channel, region, conversion_rate FROM conversion_rates ORDER BY conversion_rate DESC LIMIT 100;" 
               
     }
     ,{
         "question": "How does the revenue generated by a product vary with different advertising strategies across multiple sales channels?",
        "answer": "WITH revenue_data AS (SELECT f__channel, product_name, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY f__channel, product_name) SELECT f__channel, product_name, total_revenue FROM revenue_data ORDER BY total_revenue DESC LIMIT 100;"               
     }
      ,{
         "question": "Which promotions had the highest impact on the number of clicks and conversions across various sales channels?",
        "answer": "WITH promotion_performance AS (SELECT campaignname, SUM(clicks) AS total_clicks, SUM(conversions) AS total_conversions FROM sample_data_marketing GROUP BY campaignname) SELECT campaignname, total_clicks, total_conversions FROM promotion_performance ORDER BY total_clicks DESC, total_conversions DESC LIMIT 100;"               
     }
      ,{
         "question": "How did different sales channels perform in terms of revenue during a specific marketing campaign?",
        "answer": "SELECT sales.sales_channel_name, SUM(sales.revenue) AS total_revenue FROM sample_data_sales AS sales JOIN sample_data_marketing AS marketing ON sales.order_product_key = marketing.sku WHERE marketing.campaignname = 'specific_campaign_name' GROUP BY sales.sales_channel_name ORDER BY total_revenue DESC LIMIT 100;"               
     }
     ,{
         "question": "Which sales channels contributed the most to revenue for specific product groups during a specific ad campaign?",
        "answer": "WITH revenue_data AS (SELECT sales_channel_name, SUM(revenue) AS total_revenue FROM sample_data_sales WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY sales_channel_name) SELECT sales_channel_name, total_revenue FROM revenue_data ORDER BY total_revenue DESC LIMIT 100;"

     }
     ,{
         "question": "How does the effectiveness of promotions vary across different regions and sales channels?",
        "answer": "WITH promotion_effectiveness AS (SELECT sales_channel_name, country_name, SUM(revenue) AS total_revenue, SUM(quantity) AS total_quantity FROM sample_data_sales GROUP BY sales_channel_name, country_name) SELECT sales_channel_name, country_name, total_revenue, total_quantity FROM promotion_effectiveness ORDER BY total_revenue DESC LIMIT 100;"
                       
     }
     ,{
         "question": "What is the impact of different ad groups on revenue generated for products within specific categories?",
        "answer": "SELECT ad_group_name, SUM(revenue) AS total_revenue FROM sample_data_marketing WHERE product_group_1 IS NOT NULL GROUP BY ad_group_name ORDER BY total_revenue DESC LIMIT 100;"                 
     }
     ,{
         "question": "Which customer types (new vs. repeat) are more responsive to specific ad campaigns, and how does this vary across different sales channels?",
        "answer": "WITH ad_campaigns AS (SELECT f__channel, SUM(clicks) AS total_clicks, SUM(conversions) AS total_conversions FROM sample_data_marketing GROUP BY f__channel) SELECT f__channel, total_clicks, total_conversions, COALESCE(total_conversions / NULLIF(total_clicks, 0), 0) AS conversion_rate FROM ad_campaigns ORDER BY total_conversions DESC LIMIT 100;"                 
     }
     ,{
         "question": "Which regions had the highest revenue growth during a specific promotion, and what ad campaigns were associated with this growth?",
        "answer": "WITH promotion_data AS (SELECT country_name AS region, SUM(revenue) AS total_revenue FROM sample_data_sales WHERE order_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND CURRENT_DATE() GROUP BY country_name), previous_promotion_data AS (SELECT country_name AS region, SUM(revenue) AS total_revenue FROM sample_data_sales WHERE order_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY) AND DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY country_name), revenue_growth AS (SELECT p.region, (p.total_revenue - pp.total_revenue) / COALESCE(NULLIF(pp.total_revenue, 0), 1) AS growth_rate FROM promotion_data p JOIN previous_promotion_data pp ON p.region = pp.region) SELECT r.region, r.growth_rate, m.campaignname FROM revenue_growth r JOIN sample_data_marketing m ON r.region = m.country_code ORDER BY r.growth_rate DESC LIMIT 100;"                 
     }
      ,{
         "question": "How does the cost of goods sold (COGS) vary with different advertising strategies across various sales channels?",
        "answer": "WITH cogs_data AS (SELECT s.sales_channel_name, SUM(s.cogs) AS total_cogs, SUM(m.spend) AS total_spend FROM sample_data_sales s JOIN sample_data_marketing m ON s.order_product_key = m.sku GROUP BY s.sales_channel_name) SELECT sales_channel_name, total_cogs, total_spend, COALESCE(total_cogs / NULLIF(total_spend, 0), 0) AS cogs_per_spend FROM cogs_data ORDER BY total_cogs DESC LIMIT 100;"                 
     }
     ,{
         "question": "What is the impact of different customer types on revenue generated during specific promotions across multiple sales channels?",
        "answer": "WITH promotion_revenue AS (SELECT customer_type, SUM(revenue) AS total_revenue FROM sample_data_sales WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY customer_type) SELECT customer_type, total_revenue FROM promotion_revenue ORDER BY total_revenue DESC LIMIT 100;"                 
     }
     ,{
         "question": "Which ad campaigns generated the most revenue in a specific country, and what were the associated product groups?",
        "answer": "SELECT campaignname, SUM(revenue) AS total_revenue, product_group_1 FROM sample_data_marketing WHERE country_code = 'specific_country' GROUP BY campaignname, product_group_1 ORDER BY total_revenue DESC LIMIT 100;"                 
     }
     ,{
         "question": "How does the number of impressions correlate with revenue growth for different products across multiple sales channels?",
        "answer": "WITH impressions_revenue AS (SELECT product_name, SUM(impressions) AS total_impressions, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY product_name) SELECT product_name, total_impressions, total_revenue FROM impressions_revenue ORDER BY total_revenue DESC LIMIT 100;"                 
     }
     ,{
         "question": "Which sales channels had the highest number of conversions during a specific promotion, and what were the associated ad campaigns?",
        "answer": "WITH conversions_data AS (SELECT f__channel, SUM(conversions) AS total_conversions, campaignname FROM sample_data_marketing WHERE campaignname IS NOT NULL GROUP BY f__channel, campaignname) SELECT f__channel, total_conversions, campaignname FROM conversions_data ORDER BY total_conversions DESC LIMIT 100;"                 
     }
     ,{
         "question": "What is the relationship between the number of clicks and the revenue generated by specific products across various sales channels?",
        "answer": "WITH clicks_revenue AS (SELECT product_name, SUM(clicks) AS total_clicks, SUM(revenue) AS total_revenue FROM sample_data_marketing GROUP BY product_name) SELECT product_name, total_clicks, total_revenue FROM clicks_revenue ORDER BY total_revenue DESC LIMIT 100;"                 
     }
     ,{
         "question": "Which regions had the highest number of conversions for a specific product group during a specific ad campaign?",
        "answer": "SELECT region, SUM(conversions) AS total_conversions FROM sample_data_marketing WHERE product_group_1 = 'specific_product_group' AND campaignid = 'specific_campaign_id' GROUP BY region ORDER BY total_conversions DESC LIMIT 100;"                 
     }
     ,{
         "question": "How does the number of conversions vary with different ad spend levels across various sales channels?",
        "answer": "SELECT f__channel, SUM(conversions) AS total_conversions, SUM(spend) AS total_spend FROM sample_data_marketing GROUP BY f__channel ORDER BY total_conversions DESC LIMIT 100;"                 
     }
      ,{
         "question": "How does the number of conversions vary with different ad spend levels across various sales channels?",
        "answer": "SELECT f__channel, SUM(conversions) AS total_conversions, SUM(spend) AS total_spend FROM sample_data_marketing GROUP BY f__channel ORDER BY total_conversions DESC LIMIT 100;"                 
     }


]