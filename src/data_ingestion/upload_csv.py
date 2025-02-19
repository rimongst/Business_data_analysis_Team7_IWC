import json
import logging
import os

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Read configuration file
config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config.json")
)

with open(config_path, "r") as f:
    config = json.load(f)

# Setup Log
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_csv_to_bigquery():
    """Reading CSV and uploading to BigQuery"""
    try:
        logging.info("🔍 Read configuration file...")
        project_id = config["project_id"]
        dataset_id = config["dataset_id"]
        table_id = config["table_id"]
        csv_file_path = config["csv_file_path"]
        key_path = config["key_path"]

        # accreditation
        credentials = service_account.Credentials.from_service_account_file(key_path)
        client = bigquery.Client(credentials=credentials, project=project_id)

        # Read CSV
        logging.info(f"📂 Reading CSV files: {csv_file_path}")
        df = pd.read_csv(
            csv_file_path, encoding="utf-8", sep=";", on_bad_lines="skip", quoting=3
        )

        # Handling of column names
        df.columns = df.columns.str.strip()

        # Generate BigQuery table schema
        type_mapping = {
            "int64": "INTEGER",
            "float64": "FLOAT",
            "object": "STRING",
            "bool": "BOOLEAN",
            "datetime64[ns]": "TIMESTAMP",
        }
        schema = [
            bigquery.SchemaField(name, type_mapping.get(str(dtype), "STRING"))
            for name, dtype in df.dtypes.items()
        ]

        # Generating BigQuery Table References
        table_ref = client.dataset(dataset_id).table(table_id)

        # Delete the old table (if it exists)）
        client.delete_table(table_ref, not_found_ok=True)
        logging.info(f"🗑️ old table `{dataset_id}.{table_id}` Deleted (if present)")

        # Creating a New Table
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        logging.info(f"✅ New BigQuery Tables `{dataset_id}.{table_id}` Created！")

        # Upload data
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            schema=schema,
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
        )

        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()

        logging.info(
            f"✅ The data was successfully uploaded to the BigQuery `{dataset_id}.{table_id}`"
        )

    except Exception as e:
        logging.error(f"❌ Error: {e}")


if __name__ == "__main__":
    load_csv_to_bigquery()
