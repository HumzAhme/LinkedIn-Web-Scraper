from google.cloud import storage
import requests

BUCKET_NAME = 'hamu-storage1'

OBJECT_URL = f'https://storage.googleapis.com/storage/v1/b/{BUCKET_NAME}/o'

def upload_json(filename):
    print(f"uploading {filename} to google cloud...")
    blobname = filename
    filename = f'{filename}.json'

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)

    path = 'data/{}'.format(filename)
    blob.upload_from_filename(path)
    print(f"uploaded {filename} to {bucket}")


def download():
    'Downloads all the data in the google cloud bucket'
    data = []
    res = requests.get(OBJECT_URL)
    object_list = res.json()
    for object in object_list["items"]:
        name = object['name']
        res = requests.get(f'{OBJECT_URL}/{name}?alt=media')
        content = res.json()
        data.append((name, content))
    return data