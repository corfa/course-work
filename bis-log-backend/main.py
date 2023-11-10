from fastapi import FastAPI
import uvicorn

from routers import files

app = FastAPI()

app.include_router(files.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")

