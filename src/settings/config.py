from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings:
    def __init__(self):
        # RD Station
        self.rd_api_url = "https://crm.rdstation.com/api/v1"
        self.rd_api_token = os.getenv("RD_API_TOKEN")
        self.base_dir = BASE_DIR

        # App Control
        self.debug = os.getenv("DEBUG")

        # Microsoft
        self.ms_url = "https://login.microsoftonline.com"
        self.ms_client_id = os.getenv("MS_CLIENT_ID")
        self.ms_client_secret = os.getenv("MS_CLIENT_SECRET")
        self.ms_tenant_id = os.getenv("MS_TENANT_ID")
        self.ms_drive_id = os.getenv("MS_DRIVE_ID")

