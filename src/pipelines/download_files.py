import logging
from src.services.rdstation.rdstation import RdService
from src.settings.endpoints import ENDPOINTS_CONFIG

logger = logging.getLogger(__name__)

def download_files(rd_service: RdService, output_dir):
    logger.info("Iniciando download")

    for endpoint_name in ENDPOINTS_CONFIG:
        data = rd_service.get_data(endpoint_name)

        if not data:
            logger.warning(f"[{endpoint_name}] Sem dados")
            continue

        file_path = output_dir / f"{endpoint_name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, ensure_ascii=False, default=str)

        logger.info(f"[{endpoint_name}] {len(data)} registros salvos em {file_path}")

    logger.info("Download finalizado")