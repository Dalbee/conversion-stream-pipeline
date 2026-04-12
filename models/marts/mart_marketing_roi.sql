{{ config(materialized='table') }}

/* This model calculates estimated revenue by channel.
    Business Assumption: Each conversion is worth €50 USD to the bank.
*/

WITH conversion_stats AS (
    SELECT * FROM {{ ref('fct_banking_conversions') }}
)

SELECT
    CHANNEL,
    total_clicks,
    total_conversions,
    conversion_rate_pct,
    
    -- Financial Metrics
    (total_conversions * 50) AS estimated_revenue_usd,
    
    -- Efficiency Metric: Revenue per Click
    ROUND((total_conversions * 50.0) / NULLIF(total_clicks, 0), 2) AS revenue_per_click_usd

FROM conversion_stats
ORDER BY estimated_revenue_usd DESC