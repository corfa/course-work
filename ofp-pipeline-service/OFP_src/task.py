from minio import Minio
import requests
from OFP_src.untils import remove_artificial_pixels_in_OFP
import os
from dotenv import load_dotenv

load_dotenv()


def send_success(id_row: int):
    url = "http://"
    url += os.getenv('PATCH_URL_APP', '')
    url += str(id_row)
    data = {'status': 'done'}  
    requests.patch(url, json=data)


def remove_artificial_pixels_from_s3_file(s3_object_name: str, id_row: int):
    minio_endpoint = os.getenv('MINIO_URL', '')
    minio_access_key = os.getenv('MINIO_USER', '')
    minio_secret_key = os.getenv('MINIO_PASSWORD', '')
    bucket_name = os.getenv('BUCKET_NAME', '')
    local_file_path = s3_object_name.split("/")[-1]
    minio_client = Minio(minio_endpoint,
                         access_key=minio_access_key,
                         secret_key=minio_secret_key,
                         secure=False)

    try:
        response = minio_client.get_object(bucket_name, s3_object_name)
        with open(local_file_path, 'wb+') as local_file:
            local_file.write(response.read())
            remove_artificial_pixels_in_OFP(local_file_path)
        with open(local_file_path, 'rb') as file_data:
            minio_client.put_object(bucket_name, s3_object_name, file_data, length=os.path.getsize(local_file_path))
        os.remove(local_file_path)
        send_success(id_row)
    except Exception as e:
        raise e
