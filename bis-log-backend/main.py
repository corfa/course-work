from fastapi import FastAPI, UploadFile
from minio import Minio
from fastapi.responses import JSONResponse, RedirectResponse

import tempfile
import os
app = FastAPI()

minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,  
)


@app.post("/upload/")
async def upload_file(file: UploadFile):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.file.read())
        minio_client.fput_object("file-client", file.filename, temp_file.name, file.content_type)
        os.remove(temp_file.name)

        return JSONResponse(content={"message": "Файл успешно загружен в MinIO"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/get_file/{file_name}")
async def get_file(file_name: str):
    try:
        presigned_url = minio_client.presigned_get_object("file-client", file_name)
        return RedirectResponse(url=presigned_url)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
