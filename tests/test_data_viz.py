import pytest
import pandas as pd
from src.data_ingestion.data_viz import plot_price_distribution_by_collection

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "final_collection": ["A", "B", "A", "C"],
        "price_in_eur": [1000, 1500, 1200, 800]
    })

def test_plot_price_distribution_by_collection(sample_df):
    try:
        plot_price_distribution_by_collection(sample_df)
    except Exception as e:
        pytest.fail(f"Plot function raised an exception: {e}")
