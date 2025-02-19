import pytest
import pandas as pd
from src.data_ingestion.combine_data import combine_datasets

@pytest.fixture
def sample_data():
    df1 = pd.DataFrame({"id": [1, 2], "price": [100, 200]})
    df2 = pd.DataFrame({"id": [3, 4], "price": [300, 400]})
    return df1, df2

def test_combine_datasets(mocker, sample_data):
    mocker.patch("src.data_ingestion.combine_data.pd.read_csv", side_effect=sample_data)
    df = combine_datasets()
    assert df.shape[0] == 4  # 确保数据正确合并
