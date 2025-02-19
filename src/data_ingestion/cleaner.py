import json
import os

import pandas as pd

from data_ingestion.load_data import get_absolute_path  # ✅ 复用路径解析

# Load configuration file
config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config.json")
)
with open(config_path, "r") as f:
    config = json.load(f)


# Convert price to EUR
def convert_price_to_eur(df):
    """Convert prices to EUR using a given exchange rate dictionary."""

    exchange_rates = {
        "CHF": 1.05,
        "CNY": 0.13,
        "EUR": 1.00,
        "GBP": 1.17,
        "HKD": 0.12,
        "JPY": 0.007,
        "SGD": 0.69,
        "TWD": 0.029,
        "USD": 0.92,
        "AED": 0.25,
        "KRW": 0.0007,
    }

    if "price" in df.columns and "currency" in df.columns:
        df["price_in_eur"] = df.apply(
            lambda row: row["price"] * exchange_rates.get(row["currency"], 1)
            if pd.notna(row["price"]) and pd.notna(row["currency"])
            else None,
            axis=1,
        )
        df.dropna(subset=["price_in_eur"], inplace=True)  # 移除转换失败的行
    else:
        raise KeyError(
            "❌ Error: Columns 'price' and 'currency' are required in the dataset."
        )

    return df


# Filter potentially incorrect price data
def filter_price_outliers(df):
    """Filters out unreasonable price values to clean data."""
    if "price_in_eur" not in df.columns:
        raise KeyError(
            "❌ Error: Column 'price_in_eur' is required for filtering outliers."
        )

    df["median_price"] = df.groupby("reference_code")["price_in_eur"].transform(
        "median"
    )
    df = df[
        (df["price_in_eur"] >= 1000) & (df["price_in_eur"] >= 0.5 * df["median_price"])
    ]
    df.drop(columns=["median_price"], inplace=True, errors="ignore")

    return df


# Fix incorrect collection names
def fix_collection_names(df):
    """Fixes incorrect collection names and groups data by reference_code."""
    if "collection" in df.columns:
        df["collection_fixed"] = df["collection"].replace(
            {"HTTPS://WWW.IWC.COM/CN/ZH-CN/PAST-COLLECTIONS/PORTUGIESER": "PORTUGIESER"}
        )
        df["final_collection"] = df.groupby("reference_code")[
            "collection_fixed"
        ].transform("first")
        df.drop(columns=["collection_fixed"], inplace=True, errors="ignore")
    else:
        raise KeyError("❌ Error: Column 'collection' is missing in the dataset.")

    return df


# Full preprocessing function
def preprocess_data(df):
    """Applies all data cleaning steps to the dataset."""
    df = convert_price_to_eur(df)
    df = filter_price_outliers(df)
    df = fix_collection_names(df)
    return df


if __name__ == "__main__":
    print("🚀 Starting data cleaning...")

    try:
        # Load cleaned dataset 1
        loaded_data_1_path = get_absolute_path(config["loaded_data_1_path"])
        df1 = pd.read_csv(loaded_data_1_path)
        df1 = preprocess_data(df1)
        cleaned_data_1_path = get_absolute_path(config["cleaned_data_1_path"])
        df1.to_csv(cleaned_data_1_path, index=False)
        print(f"✅ Cleaned dataset 1 saved as '{cleaned_data_1_path}'")

        # Load cleaned dataset 2
        loaded_data_2_path = get_absolute_path(config["loaded_data_2_path"])
        df2 = pd.read_csv(loaded_data_2_path)
        df2 = preprocess_data(df2)
        cleaned_data_2_path = get_absolute_path(config["cleaned_data_2_path"])
        df2.to_csv(cleaned_data_2_path, index=False)
        print(f"✅ Cleaned dataset 2 saved as '{cleaned_data_2_path}'")

    except Exception as e:
        print(f"❌ Error: {e}")
