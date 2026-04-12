import os
import pandas as pd
import random
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# 1. Setup
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_data(n=100):
    channels = ['Paid_Social', 'Organic_Search', 'Email', 'Referral']
    events, conversions = [], []
    for i in range(n):
        uid = 5000 + i
        base_ts = datetime.now() - timedelta(days=random.randint(1, 30))
        chan = random.choice(channels)
        events.append({'USER_ID': uid, 'EVENT_NAME': 'page_view', 'TS': base_ts, 'CHANNEL': chan})
        if random.random() < 0.6:
            click_ts = base_ts + timedelta(minutes=5)
            events.append({'USER_ID': uid, 'EVENT_NAME': 'intent_click', 'TS': click_ts, 'CHANNEL': chan})
            if random.random() < 0.4:
                conversions.append({
                    'CONV_ID': f'C_{9000+i}', 
                    'USER_ID': uid, 
                    'STATUS': 'COMPLETED',
                    'CREATED_AT': click_ts + timedelta(minutes=10)
                })
    return pd.DataFrame(events), pd.DataFrame(conversions)

def run():
    try:
        df_ev, df_cv = generate_data(100)
        
        # Connect using environment variables
        conn = snowflake.connector.connect(
            user=os.getenv('SNOW_USER'),
            password=os.getenv('SNOW_PASS'),
            account=os.getenv('SNOW_ACCT'),
            warehouse=os.getenv('SNOW_WH'),
            database=os.getenv('SNOW_DB'),
            schema=os.getenv('SNOW_SCH')
        )
        
        cur = conn.cursor()
        # Explicitly create and set context
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('SNOW_DB')}")
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {os.getenv('SNOW_DB')}.{os.getenv('SNOW_SCH')}")
        cur.execute(f"USE DATABASE {os.getenv('SNOW_DB')}")
        cur.execute(f"USE SCHEMA {os.getenv('SNOW_SCH')}")
        
        logging.info("Uploading data to Snowflake...")
        
        # Use database and schema parameters inside write_pandas
        write_pandas(
            conn, 
            df_ev, 
            "STG_WEB_EVENTS", 
            database=os.getenv('SNOW_DB'), 
            schema=os.getenv('SNOW_SCH'), 
            auto_create_table=True,
            quote_identifiers=False
        )
        
        write_pandas(
            conn, 
            df_cv, 
            "STG_CRM_CONVERSIONS", 
            database=os.getenv('SNOW_DB'), 
            schema=os.getenv('SNOW_SCH'), 
            auto_create_table=True,
            quote_identifiers=False
        )
        
        logging.info("--- SUCCESS! Data is now in Snowflake ---")
        conn.close()
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run()