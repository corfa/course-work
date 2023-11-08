
from app import App
import os
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    host_app = os.getenv('HOST_APP', 'localhost')
    port_app = os.getenv('PORT_APP', '5555')
    app = App(host=host_app, port=int(port_app))
    app.run()
