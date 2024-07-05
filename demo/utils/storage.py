from google.cloud import storage
import os

# Google Service Account Key Path
# ex) "/home/user/Downloads/service-account-file.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

prefix = os.environ['BLOB_PREFIX']
bucket_name = os.environ['BUCKET_NAME']


def upload_file(file):
    file.seek(0)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(prefix + file.name)
    blob.upload_from_file(file_obj=file, content_type=file.content_type)


def get_file_list():
    storage_client = storage.Client()
    file_list = list(storage_client.list_blobs(bucket_name, prefix=prefix))
    file_list = [file.name.replace(prefix, '') for file in file_list]
    file_list.remove('')
    return file_list


def get_file_info(file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(prefix + file_name)
    uri = 'gs://' + bucket_name + '/' + prefix + file_name
    return {
        'uri': uri,
        'content_type': blob.content_type,
    }
