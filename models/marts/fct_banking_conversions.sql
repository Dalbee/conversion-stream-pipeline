{{ config(materialized='table') }}

WITH web_events AS (
    SELECT * FROM {{ ref('stg_web_events') }}
),
conversions AS (
    SELECT * FROM {{ ref('stg_crm_conversions') }}
)

SELECT
    w.CHANNEL,
    
    -- Volume Metrics
    COUNT(w.USER_ID) AS total_clicks,
    COUNT(c.CONV_ID) AS total_conversions,
    
    -- Conversion Metrics
    ROUND(COUNT(c.CONV_ID) * 100.0 / NULLIF(COUNT(w.USER_ID), 0), 2) AS conversion_rate_pct,
    
    -- Funnel Efficiency Metrics
    -- Calculates the % of users who clicked but did not complete a conversion
    ROUND((1 - (COUNT(c.CONV_ID) * 1.0 / NULLIF(COUNT(w.USER_ID), 0))) * 100, 2) AS drop_off_pct

FROM web_events w
LEFT JOIN conversions c ON w.USER_ID = c.USER_ID
WHERE w.EVENT_NAME = 'intent_click'
GROUP BY 1