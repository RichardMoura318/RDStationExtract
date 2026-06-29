# main.py
from src.applications.application import create_app
from src.settings.config import Settings
from src.settings.logger import setup_logger

settings = Settings()
setup_logger(settings.base_dir)

app = create_app(settings=settings)
app.run(download_pipe=True, upload_pipe=True)