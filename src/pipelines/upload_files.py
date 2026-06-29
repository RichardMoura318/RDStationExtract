import logging
from src.services.microsoft.services.sharepoint import SharePointService
from src.services.rdstation.endpoints import ENDPOINTS_CONFIG

logger = logging.getLogger(__name__)

def upload_files(sp_service: SharePointService, input_dir, drive_id: str, folder_path: str):
    logger.info("Iniciando upload")

    for endpoint_name in ENDPOINTS_CONFIG:
        file_path = input_dir / f"{endpoint_name}.json"

        if not file_path.exists():
            logger.warning(f"[{endpoint_name}] Arquivo não encontrado, pulando")
            continue

        content = file_path.read_bytes()

        sp_service.upload(
            drive_id=drive_id,
            folder_path=folder_path,
            file_name=f"{endpoint_name}.json",
            content=content,
        )

    logger.info("Upload finalizado")