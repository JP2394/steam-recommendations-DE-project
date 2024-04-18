from google.cloud import storage

def upload_to_gcs(file_,downloadpath,save_to=''):
    # Initialise a client
    storage_client = storage.Client("de-data-steam-recommendations")
    # Create a bucket object for our bucket
    bucket = storage_client.get_bucket('dtc_data_lake_steam')
    blob = bucket.blob(f'{save_to}{file_}')  # Assuming you want to upload to a 'raw' directory
    blob.upload_from_filename(f'{downloadpath}/{file_}')  # Upload the CSV file