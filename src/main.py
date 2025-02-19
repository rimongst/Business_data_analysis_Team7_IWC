import json
import logging
import os

import pandas as pd

from api.upload_new_exchange_rate import fetch_and_store_exchange_rates
from data_ingestion.cleaner import preprocess_data
from data_ingestion.combine_data import combine_datasets
from data_ingestion.data_viz import (plot_price_distribution_by_collection,
                                     plot_price_distribution_by_currency,
                                     plot_top_models_by_price_range)
from data_ingestion.load_data import get_absolute_path, load_data_from_csv
from data_ingestion.upload_csv import load_csv_to_bigquery
from data_ingestion.upload_to_bucket import upload_file_to_gcs

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load config file
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config.json"))
with open(config_path, "r") as f:
    config = json.load(f)

# Ensure GCP credentials are set
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config["key_path"]
    logging.info(f"🔑 GOOGLE_APPLICATION_CREDENTIALS set to {config['key_path']}")

# Exchange rate file path
EXCHANGE_RATE_FILE = get_absolute_path("data/exchange_rates.json")


def load_exchange_rates():
    """Load exchange rates from the local JSON file."""
    if not os.path.exists(EXCHANGE_RATE_FILE):
        logging.warning("⚠️ Exchange rate file not found. Fetching new rates...")
        fetch_and_store_exchange_rates()  # Get latest rates if missing

    try:
        with open(EXCHANGE_RATE_FILE, "r") as f:
            exchange_rates = json.load(f)
        logging.info(f"✅ Loaded {len(exchange_rates)} exchange rates from file.")
        return exchange_rates

    except json.JSONDecodeError:
        logging.error("❌ Corrupted exchange rate file. Fetching new rates...")
        fetch_and_store_exchange_rates()
        return load_exchange_rates()


def main():
    logging.info("🚀 Starting the BDA pipeline...")

    try:
        # Update exchange rates
        logging.info("🔄 Fetching latest exchange rates...")
        fetch_and_store_exchange_rates()
        exchange_rates = load_exchange_rates()

        # Load datasets
        logging.info("📂 Loading datasets...")
        dataset_1_path = get_absolute_path(config["dataset_1_path"])
        dataset_2_path = get_absolute_path(config["dataset_2_path"])

        df1 = load_data_from_csv(dataset_1_path, sep=",")
        df2 = load_data_from_csv(dataset_2_path, sep=";")

        loaded_data_1_path = get_absolute_path(config["loaded_data_1_path"])
        loaded_data_2_path = get_absolute_path(config["loaded_data_2_path"])

        df1.to_csv(loaded_data_1_path, index=False)
        df2.to_csv(loaded_data_2_path, index=False)
        logging.info(
            f"✅ Datasets saved as '{loaded_data_1_path}' and '{loaded_data_2_path}'."
        )

        # Clean data with latest exchange rates
        logging.info("🧹 Cleaning datasets...")
        df1_cleaned = preprocess_data(df1, exchange_rates)
        df2_cleaned = preprocess_data(df2, exchange_rates)

        cleaned_data_1_path = get_absolute_path(config["cleaned_data_1_path"])
        cleaned_data_2_path = get_absolute_path(config["cleaned_data_2_path"])

        df1_cleaned.to_csv(cleaned_data_1_path, index=False)
        df2_cleaned.to_csv(cleaned_data_2_path, index=False)
        logging.info(
            f"✅ Cleaned datasets saved as '{cleaned_data_1_path}' and '{cleaned_data_2_path}'."
        )

        # Merge data
        logging.info("🔄 Merging datasets...")
        combined_df = combine_datasets()
        combined_data_path = get_absolute_path(config["combined_data_path"])
        combined_df.to_csv(combined_data_path, index=False)
        logging.info(f"✅ Combined dataset saved as '{combined_data_path}'.")

        # Visualization
        logging.info("📊 Generating visualizations...")
        plot_price_distribution_by_collection(combined_df)
        plot_top_models_by_price_range(combined_df)

        # Select a valid reference code
        valid_reference_codes = combined_df["reference_code"].dropna().unique()
        if len(valid_reference_codes) > 0:
            sample_reference_code = valid_reference_codes[0]
            plot_price_distribution_by_currency(
                combined_df, reference_code=sample_reference_code
            )
        else:
            logging.warning(
                "⚠️ No valid reference codes found for currency visualization."
            )

        # Upload to BigQuery
        logging.info("☁️ Uploading data to BigQuery...")
        load_csv_to_bigquery()
        logging.info("✅ Data upload complete.")

        # Upload image to Google Cloud Storage (GCS)
        logging.info("🖼️ Uploading image to Google Cloud Storage (GCS)...")
        image_path = get_absolute_path(config["local_file_path"])
        bucket_name = config["bucket_name"]
        destination_blob_name = config["destination_blob_name"]

        upload_file_to_gcs(image_path, bucket_name, destination_blob_name)
        logging.info(f"✅ Image uploaded to GCS bucket '{bucket_name}' as '{destination_blob_name}'.")

        logging.info("🎉 BDA pipeline completed successfully!")

    except Exception as e:
        logging.error(f"❌ Error in the BDA pipeline: {e}")


if __name__ == "__main__":
    main()
