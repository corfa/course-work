from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pika.adapters.blocking_connection import BlockingChannel
from fastapi import UploadFile
from broker.actions import put_in_queue

from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

import tempfile
import os

from routers.depends import get_db, verification, get_minio_client, get_broker
from db.requests.files_req import create_file_row, get_all_users_files,get_username, update_file_status

import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

bucket_name = access_key=os.getenv('BUCKET_NAME', '')

@router.post("/upload/")
async def upload_file(file: UploadFile, minio_client=Depends(get_minio_client), db=Depends(get_db), token=Depends(verification), broker: BlockingChannel = Depends(get_broker)):
    try:
        username = get_username(db,token["id"])
        object_name = f"{username}/{file.filename}"
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.file.read())
        
        minio_client.fput_object(bucket_name, object_name, temp_file.name, file.content_type)
        os.remove(temp_file.name)

        row_id = create_file_row(db, object_name, token["id"])

        put_in_queue(broker, object_name, row_id)

        return JSONResponse(content={"message": row_id})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@router.get("/get/file/{file_name}")
async def get_file(file_name: str,db=Depends(get_db),minio_client=Depends(get_minio_client), token: dict = Depends(verification)):
    try:
        username = get_username(db, token["id"])
        object_name = f"{username}/{file_name}"
        file_data = minio_client.get_object(bucket_name, object_name).data
        return StreamingResponse(content=iter([file_data]), media_type="image/tiff", headers={"Content-Disposition": f"attachment; filename={file_name}"})



    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/get/all/files")
async def get_file(db: Session = Depends(get_db), token: dict = Depends(verification)):
    try:
        files = get_all_users_files(db, token["id"])
        return JSONResponse(content={"all_files": files})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@router.patch("/update/file/status/{file_id}")
async def get_file(file_id: int, request_data: dict, db: Session = Depends(get_db)):
    try:
        if "status_file" in request_data:
            status_file = request_data["status_file"]
            status_res = update_file_status(db, file_id, status_file)
            return JSONResponse(content={"status": status_res})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
