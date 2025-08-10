from google.cloud import storage
import os

# creds for laptop
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Yu Zen\Documents\Coding\sapient-metrics-436909-v6-09e1f1ee28c1.json"
# for desktop
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\cheah\OneDrive\Documents\Coding\sapient-metrics-436909-v6-09e1f1ee28c1.json"


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
# Path to laptop folder
# local_destination = r"C:\Users\Yu Zen\Documents\Coding\Project-JBridge\GCloud\blahblah"
# to dekstop folder
local_destination = r"C:\Users\cheah\OneDrive\Documents\Coding\Project-JBridge\GCloud\all_snaps\06-28_11-00_Sat_MOREEEE"

download_folder(bucket_name, folder_name, local_destination)
