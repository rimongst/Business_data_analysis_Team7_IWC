import pytest
import pandas as pd
from io import StringIO
from src.data_ingestion.load_data import load_data_from_csv

@pytest.fixture
def csv_data():
    return "id,price\n1,100\n2,200\n"

def test_load_data_from_csv(mocker, csv_data):
    mocker.patch("builtins.open", return_value=StringIO(csv_data))
    mocker.patch("os.path.exists", return_value=True)

    df = load_data_from_csv("dummy_path.csv")
    assert df.shape == (2, 2)
    assert "id" in df.columns and "price" in df.columns
