from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from routers import files

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
app.include_router(files.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
