from minio import Minio
import requests

import os
from dotenv import load_dotenv

load_dotenv()


def send_count_words(count_words: int, id_row:int):
    url = "http://"
    url += os.getenv('PATCH_URL_APP', '')
    url += str(id_row)
    data = {'count_words': count_words}  
    res = requests.patch(url, json=data)


def count_words_in_file(file_content):
    words = file_content.split()
    return len(words)


def get_count_words_from_s3_file(patch_s3: str, id_row: int):
    minio_endpoint = os.getenv('MINIO_URL', '')
    minio_access_key = os.getenv('MINIO_USER', '')
    minio_secret_key = os.getenv('MINIO_PASSWORD', '')
    bucket_name = os.getenv('BUCKET_NAME', '')
    minio_client = Minio(minio_endpoint,
                         access_key=minio_access_key,
                         secret_key=minio_secret_key,
                         secure=False)

    try:
        response = minio_client.get_object(bucket_name, patch_s3)
        file_content = response.read().decode('utf-8')
        word_count = count_words_in_file(file_content)
        send_count_words(word_count,id_row)
        print(f"Word count in the file: {word_count}")
    except Exception as e:
        print(f"Error: {e}")


