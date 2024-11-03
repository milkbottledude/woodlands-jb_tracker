from google.cloud import storage
import os

# downloading stuff in folder from bucket
def download_folder(bucket_name, folder_name, local_destination):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # List all blobs in the specified folder
    blobs = bucket.list_blobs(prefix=folder_name)

    for blob in blobs:
        if blob.name == folder_name:
            continue
        # Create a local path for each file
        b4join = blob.name[len(folder_name):].lstrip('/')
        local_file_path = os.path.join(local_destination, b4join)
        # Download the blob to the local file
        blob.download_to_filename(local_file_path)
        print(f"Downloaded {blob.name} to {local_file_path}")

# Example usage
bucket_name = "frickubucket"
folder_name = "snapshots/"  # Ensure it ends with a slash
local_destination = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\snaps"  # Path to your 'ballsy' folder

download_folder(bucket_name, folder_name, local_destination)
