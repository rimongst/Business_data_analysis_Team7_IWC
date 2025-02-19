import json
import logging
import os

import pandas as pd

from data_ingestion.cleaner import preprocess_data
from data_ingestion.combine_data import combine_datasets
from data_ingestion.data_viz import (plot_price_distribution_by_collection,
                                     plot_price_distribution_by_currency,
                                     plot_top_models_by_price_range)
from data_ingestion.load_data import get_absolute_path, load_data_from_csv
from data_ingestion.upload_csv import load_csv_to_bigquery

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load config file
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config.json"))
with open(config_path, "r") as f:
    config = json.load(f)


def main():
    logging.info("🚀 Starting the BDA pipeline...")

    try:
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

        # Clean data
        logging.info("🧹 Cleaning datasets...")
        df1_cleaned = preprocess_data(df1)
        df2_cleaned = preprocess_data(df2)

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

        logging.info("🎉 BDA pipeline completed successfully!")

    except Exception as e:
        logging.error(f"❌ Error in the BDA pipeline: {e}")


if __name__ == "__main__":
    main()
