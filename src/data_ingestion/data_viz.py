import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load configuration file
config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config.json")
)
with open(config_path, "r") as f:
    config = json.load(f)


# Convert relative path (from config.json) to absolute path
def get_absolute_path(relative_path):
    """Convert relative data path to absolute path."""
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )  # 确保 `BDA/` 作为根目录
    absolute_path = os.path.join(base_dir, relative_path)
    print(
        f"🔍 Resolving path: {relative_path} → {absolute_path}"
    )  # ✅ Debugging path resolution
    return absolute_path


# Price Distribution by Collection
def plot_price_distribution_by_collection(df):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="final_collection", y="price_in_eur", palette="tab10")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Collection")
    plt.ylabel("Price in EUR")
    plt.title("Price Distribution by Collection")
    plt.show()


# Top Models by Price Range
def plot_top_models_by_price_range(df, top_n=20):
    price_ranges = df.groupby("reference_code")["price_in_eur"].agg(
        lambda x: x.max() - x.min()
    )
    top_range_models = price_ranges.nlargest(top_n).index
    df_top_range = df[df["reference_code"].isin(top_range_models)]

    plt.figure(figsize=(14, 6))
    sns.boxplot(
        data=df_top_range, x="reference_code", y="price_in_eur", palette="tab10"
    )
    plt.xticks(rotation=45, ha="right")
    plt.xlabel(f"Top {top_n} Models with Biggest Price Range")
    plt.ylabel("Price in EUR")
    plt.title(f"Price Distribution for Top {top_n} Models with Highest Price Range")
    plt.show()


# Price Distribution by Currency
def plot_price_distribution_by_currency(df, reference_code):
    plt.figure(figsize=(10, 5))
    sns.boxplot(
        data=df[df["reference_code"] == reference_code],
        x="currency",
        y="price_in_eur",
        palette="Set2",
    )
    plt.xlabel("Currency")
    plt.ylabel("Price in EUR")
    plt.title(f"Price Distribution for {reference_code} by Currency")
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    print("🚀 Loading combined dataset...")

    # Load the combined dataset using absolute path
    combined_data_path = get_absolute_path(config["combined_data_path"])
    print(f"📂 Loading dataset: {combined_data_path}")

    try:
        combined_df = pd.read_csv(combined_data_path)
        print(
            f"✅ Successfully loaded {combined_df.shape[0]} rows and {combined_df.shape[1]} columns."
        )
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        exit(1)

    # Run visualizations
    plot_price_distribution_by_collection(combined_df)
    plot_top_models_by_price_range(combined_df)

    # Select a reference code for visualization
    valid_reference_codes = combined_df["reference_code"].dropna().unique()
    if len(valid_reference_codes) > 0:
        sample_reference_code = valid_reference_codes[0]  # 选择第一个非空的参考代码
        plot_price_distribution_by_currency(
            combined_df, reference_code=sample_reference_code
        )
    else:
        print("⚠️ Warning: No valid reference codes found for currency visualization.")
