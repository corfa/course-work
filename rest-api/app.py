import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db.session_db import check_db_connect
from routers import user, email


class App:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = FastAPI()
        self.server.add_middleware(CORSMiddleware,
                                   allow_origins=["*"],
                                   allow_credentials=True,
                                   allow_methods=["*"],
                                   allow_headers=["*"],
                                   )

    def run(self):
        check_db_connect()
        self.server.include_router(user.router)
        self.server.include_router(email.router)
        uvicorn.run(self.server, host=self.host, port=self.port)
