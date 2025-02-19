import json
import os

import pandas as pd

from data_ingestion.cleaner import get_absolute_path  # ✅ 复用路径解析
from data_ingestion.load_data import load_data_from_csv

# Load configuration file
config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config.json")
)
with open(config_path, "r") as f:
    config = json.load(f)


def combine_datasets():
    """Loads cleaned datasets and merges them."""
    print("🚀 Starting data merging...")

    try:
        # Load cleaned dataset 1
        cleaned_data_1_path = get_absolute_path(config["cleaned_data_1_path"])
        print(f"📂 Loading cleaned dataset 1: {cleaned_data_1_path}")
        df1 = pd.read_csv(cleaned_data_1_path)
        print(f"✅ Cleaned dataset 1 loaded successfully: {df1.shape[0]} rows.")

        # Load cleaned dataset 2
        cleaned_data_2_path = get_absolute_path(config["cleaned_data_2_path"])
        print(f"📂 Loading cleaned dataset 2: {cleaned_data_2_path}")
        df2 = pd.read_csv(cleaned_data_2_path)
        print(f"✅ Cleaned dataset 2 loaded successfully: {df2.shape[0]} rows.")

        # Ensure matching columns
        missing_columns = set(df1.columns) - set(df2.columns)
        if missing_columns:
            print(f"⚠️ Warning: Columns missing in dataset 2: {missing_columns}")
            df2 = df2.reindex(columns=df1.columns, fill_value=None)  # 填充缺失列

        # Merge datasets
        combined_df = pd.concat([df1, df2], ignore_index=True)
        print(
            f"🔄 Merging completed. Final dataset contains {combined_df.shape[0]} rows."
        )

        # Save combined dataset
        combined_data_path = get_absolute_path(config["combined_data_path"])
        combined_df.to_csv(combined_data_path, index=False)
        print(f"✅ Combined dataset saved as '{combined_data_path}'")

        return combined_df

    except Exception as e:
        print(f"❌ Error during data merging: {e}")
        return None


if __name__ == "__main__":
    combined_df = combine_datasets()
    if combined_df is not None:
        print("✅ Data merge complete. Ready for next steps!")
