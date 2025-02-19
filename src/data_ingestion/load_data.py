import json
import os

import pandas as pd

# Load configuration file
config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../config.json")
)
with open(config_path, "r") as f:
    config = json.load(f)


# Convert relative path (from config.json) to absolute path
def get_absolute_path(relative_path):
    """Convert relative data path to absolute path."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    absolute_path = os.path.join(base_dir, relative_path)
    print(
        f"🔍 Resolving path: {relative_path} → {absolute_path}"
    )  # ✅ Debugging path resolution
    return absolute_path


# Load data from a CSV file
def load_data_from_csv(file_path, sep=","):
    """Loads dataset from a specified CSV file."""
    file_path = get_absolute_path(file_path)

    print(f"📂 Looking for file at: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"❌ Error: File '{file_path}' not found at absolute path: {file_path}"
        )

    try:
        df = pd.read_csv(file_path, sep=sep, engine="python")  # ✅ 显式指定 `sep` 解析符
        df.columns = df.columns.str.strip()  # ✅ 去除列名空格
        print(
            f"✅ Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns from {file_path}"
        )
        print(f"📝 Columns: {df.columns.tolist()}")  # ✅ 显示解析后的列名
        return df
    except Exception as e:
        raise ValueError(f"❌ Error loading CSV file: {e}")


if __name__ == "__main__":
    print("🚀 Starting data loading...")

    try:
        # Load dataset 1 with correct separator
        df1 = load_data_from_csv(config["dataset_1_path"], sep=",")  # ✅ 指定 `,` 作为分隔符
        loaded_data_1_path = get_absolute_path(config["loaded_data_1_path"])
        df1.to_csv(loaded_data_1_path, index=False)
        print(f"✅ Dataset 1 loaded and saved as '{loaded_data_1_path}'")
        print(df1.head())

        # Load dataset 2 (use ";" if necessary)
        df2 = load_data_from_csv(
            config["dataset_2_path"], sep=","
        )  # ✅ dataset_2.csv 可能用 `;`
        loaded_data_2_path = get_absolute_path(config["loaded_data_2_path"])
        df2.to_csv(loaded_data_2_path, index=False)
        print(f"✅ Dataset 2 loaded and saved as '{loaded_data_2_path}'")

    except Exception as e:
        print(f"❌ Error: {e}")
