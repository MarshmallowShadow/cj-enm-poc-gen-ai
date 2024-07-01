from google.cloud import storage
import os

# Google Service Account Credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""


def upload_file(file):
    file.seek(0)
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ['BUCKET_NAME'])
    blob = bucket.blob(file.name)
    blob.upload_from_file(file)
