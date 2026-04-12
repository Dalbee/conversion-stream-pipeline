import os
from datetime import datetime
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

PROJECT_PATH = "/usr/app"

# We define the profile mapping separately to ensure it's clean
profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_default",
        profile_args={
            "database": os.getenv("SNOW_DB"),
            "schema": os.getenv("SNOW_SCH"),
            "warehouse": os.getenv("SNOW_WH"),
        },
    ),
)

# Use the DbtDag class as a variable named 'dag' or similar
# Airflow looks for any object of type DAG in the global scope
banking_transformation_pipeline = DbtDag(
    project_config=ProjectConfig(
        # Pass the path as the first positional argument
        PROJECT_PATH, 
        project_name="conversion_stream_pipeline",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path="/usr/local/bin/dbt",
    ),
    render_config=RenderConfig(
        select=["path:models"],
    ),
    operator_args={"install_deps": False},
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    dag_id="banking_transformation_pipeline",
)