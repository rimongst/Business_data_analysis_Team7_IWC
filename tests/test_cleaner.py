import pytest
import pandas as pd
from src.data_ingestion.cleaner import convert_price_to_eur, filter_price_outliers, fix_collection_names

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "price": [100, 200, 300, None],
        "currency": ["USD", "EUR", "GBP", "CNY"],
        "reference_code": ["A1", "A1", "B2", "B2"],
        "collection": ["HTTPS://WWW.IWC.COM/CN/ZH-CN/PAST-COLLECTIONS/PORTUGIESER", "PORTUGIESER", "PILOT", "AQUATIMER"]
    })

def test_convert_price_to_eur(sample_df):
    df = convert_price_to_eur(sample_df)
    assert "price_in_eur" in df.columns
    assert df["price_in_eur"].notnull().sum() == 3  # 只有非空价格应被转换

def test_filter_price_outliers(sample_df):
    sample_df["price_in_eur"] = [5000, 10000, 50, 20000]  # 人工创建异常值
    df = filter_price_outliers(sample_df)
    assert all(df["price_in_eur"] >= 1000)

def test_fix_collection_names(sample_df):
    df = fix_collection_names(sample_df)
    assert "final_collection" in df.columns
    assert df["final_collection"].iloc[0] == "PORTUGIESER"
