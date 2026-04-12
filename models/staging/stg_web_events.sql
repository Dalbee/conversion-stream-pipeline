SELECT 
    USER_ID,
    EVENT_NAME,
    CHANNEL,
    TO_TIMESTAMP(TS) as event_at
FROM {{ source('landing', 'stg_web_events') }}