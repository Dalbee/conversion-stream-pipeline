{{ config(materialized='view') }}

-- This model identifies users who clicked but never converted
-- Use this list for Marketing re-targeting campaigns

WITH web_events AS (
    SELECT 
        USER_ID,
        CHANNEL,
        event_at
    FROM {{ ref('stg_web_events') }}
    WHERE EVENT_NAME = 'intent_click'
),

conversions AS (
    SELECT 
        USER_ID
    FROM {{ ref('stg_crm_conversions') }}
)

SELECT
    w.USER_ID,
    w.CHANNEL,
    w.event_at AS click_timestamp
FROM web_events w
LEFT JOIN conversions c ON w.USER_ID = c.USER_ID
WHERE c.USER_ID IS NULL -- Filter for those who did NOT convert