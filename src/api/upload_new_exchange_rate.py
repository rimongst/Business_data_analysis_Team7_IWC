import json
import os
import requests

# 获取项目根目录
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
EXCHANGE_RATE_FILE = os.path.join(BASE_DIR, "data/exchange_rates.json")


def fetch_and_store_exchange_rates():
    """
    Fetch real-time exchange rates and save them to a JSON file.
    """
    api_key = "39eda832a94011840617e68f"  # 替换成你的 API Key
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/EUR"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error if request fails

        data = response.json()
        rates = data.get("conversion_rates", {})

        if not rates:
            print("⚠️ Warning: API returned empty exchange rates.")
            return False

        # 保存到 JSON 文件
        with open(EXCHANGE_RATE_FILE, "w") as f:
            json.dump(rates, f, indent=4)

        print(f"✅ Exchange rates saved to {EXCHANGE_RATE_FILE}")
        return True

    except requests.RequestException as e:
        print(f"❌ Error fetching exchange rates: {e}")
        return False


if __name__ == "__main__":
    fetch_and_store_exchange_rates()
