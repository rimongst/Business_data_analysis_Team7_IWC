from google.cloud import storage
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Check if the environment variable has been loaded successfully
print("🔍 GCP Key Path:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# Specify GCP project ID (optional, if you need to explicitly define it in this script)
project_id = "my-new-luxury-project"

# Prepare the file to upload and the target Bucket
local_file_path = "/Users/gaoshitan/Desktop/IW328210-pilot-mark-xx-intro-desktop.png.transform.global_image_1920_2x.avif"  # Local file path to upload (image/text/any format)
bucket_name = "luxurybucketgourp7"  # Name of the Bucket you created/are using in GCP console
destination_blob_name = "images/my_watch_image.png"  
# This is the 'object name' in the Bucket, similar to a path in the cloud storage. You can customize it, e.g., placing it in an 'images' folder

def upload_file_to_gcs(local_path, bucket_name, blob_name):
    # Initialize the client
    storage_client = storage.Client(project=project_id)
    # Get the specified Bucket
    bucket = storage_client.bucket(bucket_name)
    # Create a Blob object to represent the storage location in GCS
    blob = bucket.blob(blob_name)
    
    # Upload the file
    try:
        blob.upload_from_filename(local_path)
        print(f"✅ File '{local_path}' uploaded to 'gs://{bucket_name}/{blob_name}'")
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")

if __name__ == "__main__":
    upload_file_to_gcs(local_file_path, bucket_name, destination_blob_name)