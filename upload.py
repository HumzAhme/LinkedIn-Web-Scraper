from google.cloud import storage

BUCKET_NAME = 'hamu-storage1'

def upload_json(filename):
    print(f"uploading {filename} to google cloud...")
    blobname = filename.split('.')[0]

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)

    path = 'data/{}'.format(filename)
    blob.upload_from_filename(path)
    print(f"uploaded {filename} to {bucket}")