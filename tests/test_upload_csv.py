import pytest
from unittest import mock
from src.data_ingestion.upload_csv import load_csv_to_bigquery


@pytest.fixture
def mock_bigquery_client(mocker):
    mock_client = mocker.patch("google.cloud.bigquery.Client")
    return mock_client


def test_load_csv_to_bigquery(mock_bigquery_client, mocker):
    mocker.patch("pandas.read_csv", return_value=pd.DataFrame({"id": [1, 2]}))

    try:
        load_csv_to_bigquery()
        assert mock_bigquery_client.called  # 确保 BigQuery 客户端被调用
    except Exception as e:
        pytest.fail(f"BigQuery upload function failed: {e}")
