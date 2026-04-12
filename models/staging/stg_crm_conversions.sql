SELECT 
    USER_ID,
    CONV_ID,
    STATUS,
    TO_TIMESTAMP(CREATED_AT) as converted_at
FROM {{ source('landing', 'stg_crm_conversions') }}