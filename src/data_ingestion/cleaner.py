import json
import os

import pandas as pd

from data_ingestion.load_data import get_absolute_path


EXCHANGE_RATE_FILE = get_absolute_path("data/exchange_rates.json")

# Load configuration file
config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config.json")
)
with open(config_path, "r") as f:
    config = json.load(f)

def load_exchange_rates():
    """
    Load exchange rates from exchange_rates.json.
    If the file is missing or corrupted, fallback to default rates.
    """
    if not os.path.exists(EXCHANGE_RATE_FILE):
        print("⚠️ Warning: Exchange rate file not found. Using default values.")
        return None

    try:
        with open(EXCHANGE_RATE_FILE, "r") as f:
            exchange_rates = json.load(f)
        print(f"✅ Loaded {len(exchange_rates)} exchange rates from file.")
        return exchange_rates

    except json.JSONDecodeError:
        print("❌ Error: Corrupted exchange rate file. Using default values.")
        return None


# Convert price to EUR
def convert_price_to_eur(df, exchange_rates):
    """
    Convert prices to EUR using exchange rates from file.
    If file is missing, falls back to default exchange rates.
    """
    exchange_rates = load_exchange_rates()

    # If no valid rates, fallback to defaults
    if exchange_rates is None:
        exchange_rates = {
            "CHF": 0.94, "CNY": 7.61, "EUR": 1.00, "GBP": 0.83,
            "HKD": 8.12, "JPY": 158.74, "SGD": 1.40, "TWD": 34.22,
            "USD": 1.05, "AED": 3.84, "KRW": 1506.98,
        }
        print("⚠️ Using hardcoded fallback exchange rates.")

    # Apply conversion
    if "price" in df.columns and "currency" in df.columns:
        df["price_in_eur"] = df.apply(
            lambda row: row["price"] / exchange_rates.get(row["currency"], 1)
            if pd.notna(row["price"]) and pd.notna(row["currency"])
            else None,
            axis=1,
        )
        df.dropna(subset=["price_in_eur"], inplace=True)
    else:
        raise KeyError("❌ Error: Columns 'price' and 'currency' are required in the dataset.")

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
def preprocess_data(df, exchange_rates):
    """Applies all data cleaning steps to the dataset, using real exchange rates."""
    df = convert_price_to_eur(df, exchange_rates)
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
