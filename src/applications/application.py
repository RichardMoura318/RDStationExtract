# application.py
import logging
from src.services.microsoft.client import MicrosoftClient
from src.services.rdstation.client import RdClient
from src.services.rdstation.rdstation import RdService
from src.services.microsoft.sharepoint import SharePointService
from src.settings.config import Settings
from src.pipelines.download_files import download_files
from src.pipelines.upload_files import upload_files

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, rd_service: RdService, sp_service: SharePointService, settings: Settings):
        self.rd_service = rd_service
        self.sp_service = sp_service
        self.data_dir = settings.base_dir / "data"

    def run(self, download_pipe: bool = True, upload_pipe: bool = True):
        logger.info("Iniciando aplicação")

        folder_path = "JSON"
        drive_id = "b!WlCZxHNF3UySOdx-lzudeR31iGFRBDtAl6mG_Nh3uDmTCLEjqyQ9T5fDU-U8zCWS"

        if download_pipe:
            download_files(rd_service=self.rd_service, output_dir=self.data_dir)

        if upload_pipe:
            upload_files(sp_service=self.sp_service, drive_id=drive_id, folder_path=folder_path, input_dir=self.data_dir)

        logger.info("Aplicação finalizada")


def create_app(settings: Settings) -> Application:
    site_id = "recursus.sharepoint.com,c499505a-4573-4cdd-9239-dc7e973b9d79,6188f51d-0451-403b-97a9-86fcd877b839"

    ms_client = MicrosoftClient(settings)
    rd_client = RdClient(settings)

    rd_service = RdService(rd_client)
    sp_service = SharePointService(ms_client,site_id=site_id)

    return Application(rd_service, sp_service, settings)