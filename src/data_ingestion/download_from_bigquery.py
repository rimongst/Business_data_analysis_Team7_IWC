import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Set your GCP project ID
project_id = "my-new-luxury-project"

# Define SQL query to download data from iwc_prices table
query = """
SELECT 
  *
FROM `my-new-luxury-project.luxury_watch_data.iwc_prices`
"""

# Initialize BigQuery client
client = bigquery.Client(project=project_id)

try:
    # Run query and convert result to pandas DataFrame
    df = client.query(query).to_dataframe()
    
    # Export the DataFrame to a CSV file
    output_file_path = 'iwc_prices_data.csv'
    df.to_csv(output_file_path, index=False)
    print(f"Data from iwc_prices has been downloaded and saved to {output_file_path}")
    
    # Optionally, print the first few rows to verify
    print(df.head())
except Exception as e:
    # If an error occurs, print it for debugging
    print(f"An error occurred: {str(e)}")