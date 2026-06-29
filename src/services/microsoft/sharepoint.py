from src.services.microsoft.client import MicrosoftClient
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)

logger = logging.getLogger(__name__)


class SharePointService:
    def __init__(self, client: MicrosoftClient, site_id: str = None):
        self.client = client
        self.site_id = site_id

    def get_drives(self) -> list:
        response = self.client.get(f"sites/{self.site_id}/drives")

        if response.get("status") != "success":
            logger.error(f"Erro ao buscar drives: {response.get('message')}")
            return []

        drives = response.get("data", {}).get("value", [])

        logger.info(f"Drives encontrados: {drives}")

        return drives

    def get_lists(self) -> list:
        response = self.client.get(f"sites/{self.site_id}/lists")

        if response.get("status") != "success":
            logger.error(f"Erro ao buscar listas: {response.get('message')}")
            return []

        lists = response.get("data", {}).get("value", [])

        logger.info(f"Listas encontradas: {len(lists)}")

        return lists

    def list_files(self, path_name: str, drive_id: str) -> list:
        response = self.client.get(f"drives/{drive_id}/root:/{path_name}:/children")

        if response.get("status") != "success":
            logger.error(f"Erro ao listar arquivos: {response.get('message')}")
            return []

        return response.get("data", {}).get("value", [])

    def upload(
        self, drive_id: str, folder_path: str, file_name: str, content: bytes
    ) -> dict:
        response = self.client.put(
            endpoint=f"drives/{drive_id}/root:/{folder_path}/{file_name}:/content",
            data=content,
        )

        if response.get("status") != "success":
            logger.error(f"Erro ao fazer upload: {response.get('message')}")
            return {}

        logger.info(f"Arquivo {file_name} enviado com sucesso")
        return response.get("data", {})

    def download_file(
        self, drive_id: str, folder_path: str, file_name: str, save_path: str = None
    ) -> bytes:
        response = self.client.get(
            endpoint=f"drives/{drive_id}/root:/{folder_path}/{file_name}:/content",
            raw=True,
        )

        if response.get("status") != "success":
            logger.error(f"Erro ao baixar arquivo: {response.get('message')}")
            return b""

        content = response.get("data")

        if save_path:
            with open(save_path, "wb") as f:
                f.write(content)
            logger.info(f"Arquivo {file_name} salvo em: {save_path}")
        else:
            logger.info(f"Arquivo {file_name} baixado com sucesso")

        return content

    def list_items(self, list_id: str) -> list:
        all_items = []
        endpoint = f"sites/{self.site_id}/lists/{list_id}/items?expand=fields"

        while endpoint:
            response = self.client.get(endpoint=endpoint)

            if response.get("status") != "success":
                logger.error(f"Erro ao listar itens: {response.get('message')}")
                break

            data = response.get("data", {})
            items = data.get("value", [])
            all_items.extend([item.get("fields", {}) for item in items])

            next_link = data.get("@odata.nextLink")

            if next_link:
                # nextLink já é a URL completa, remove o base para usar só o endpoint
                endpoint = next_link.replace("https://graph.microsoft.com/v1.0/", "")
                logger.debug(f"Próxima página... total até agora: {len(all_items)}")
            else:
                endpoint = None

        logger.info(f"Total de itens coletados: {len(all_items)}")
        return all_items

    def insert_item(self, list_id: str, fields: dict) -> dict:
        response = self.client.post(
            endpoint=f"sites/{self.site_id}/lists/{list_id}/items",
            data={"fields": fields},
        )

        if response.get("status") != "success":
            logger.error(f"Erro ao inserir item: {response.get('message')}")
            return {}

        item_id = response.get("data", {}).get("id")
        logger.info(f"Item inserido com sucesso. ID: {item_id}")
        return response.get("data", {})

    def update_item(self, list_id: str, item_id: str, fields: dict) -> dict:
        response = self.client.patch(
            endpoint=f"sites/{self.site_id}/lists/{list_id}/items/{item_id}/fields",
            data=fields,
        )

        if response.get("status") != "success":
            logger.error(f"Erro ao atualizar item: {response.get('message')}")
            return {}

        logger.info(f"Item {item_id} atualizado com sucesso")
        return response.get("data", {})

if __name__ == "__main__":
    from src.settings.config import Settings

    settings = Settings()
    client = MicrosoftClient(settings=settings)
    sharepoint = SharePointService(
        client=client,
        site_id="recursus.sharepoint.com,c499505a-4573-4cdd-9239-dc7e973b9d79,6188f51d-0451-403b-97a9-86fcd877b839"
    )

    # primeiro descobre as listas disponíveis
    print("=== LISTAS ===")
    drivers = sharepoint.get_drives()

    print(drivers)