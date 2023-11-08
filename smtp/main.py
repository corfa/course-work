from app import AppConfig
from app.app import App

if __name__ == '__main__':
    config = AppConfig()
    app = App(config=config)
    app.run()
