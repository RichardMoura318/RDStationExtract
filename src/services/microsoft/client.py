import requests
import logging
from src.settings.config import Settings
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%d/%m/%y %H:%M:%S"
)

logger = logging.getLogger(__name__)

GRAPH_URL = "https://graph.microsoft.com/v1.0"


def handle_response(response: requests.Response, raw: bool = False) -> dict:
    if raw:
        return {"status": "success", "data": response.content}
    return {
        "status": "success",
        "data": response.json() if response.content else {}
    }


def handle_error(endpoint: str, e: Exception) -> dict:
    logger.error(f"[{endpoint}] error: {e}")
    return {"status": "erro", "message": str(e)}


class MicrosoftClient:
    def __init__(self, settings: Settings):
        self.auth_url = settings.ms_url
        self.client_id = settings.ms_client_id
        self.client_secret = settings.ms_client_secret
        self.tenant_id = settings.ms_tenant_id

        self.access_token = None
        self.token_window_end = None

        self.session = requests.Session()

    def _check_token(self):
        if not self.access_token or datetime.now() >= self.token_window_end:
            logger.info("Token expirado, renovando...")
            self._get_graph_token()

    def _get_graph_token(self):
        logger.info("Obtendo novo token do Graph")

        url = f"{self.auth_url}/{self.tenant_id}/oauth2/v2.0/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default"
        }

        try:
            response = requests.post(
                url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30
            )
            response.raise_for_status()
            response_json = response.json()

            token = response_json.get("access_token")
            expires_in = int(response_json.get("expires_in"))

            if token:
                self.access_token = token
                self.token_window_end = datetime.now() + timedelta(seconds=expires_in)
                self.session.headers.update({
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                })
                logger.info(f"Token obtido com sucesso. Expira em {expires_in}s")

        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro ao obter o token: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão ao obter token: {e}")

    def get(self, endpoint: str, params: dict = None, raw: bool = False) -> dict:
        self._check_token()
        url = f"{GRAPH_URL}/{endpoint}"
        try:
            response = self.session.get(url=url, params=params, timeout=30)
            response.raise_for_status()
            return handle_response(response, raw)
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            return handle_error(endpoint, e)

    def post(self, endpoint: str, data: dict) -> dict:
        self._check_token()
        url = f"{GRAPH_URL}/{endpoint}"
        try:
            response = self.session.post(url=url, json=data, timeout=30)
            response.raise_for_status()
            return handle_response(response)
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            return handle_error(endpoint, e)

    def put(self, endpoint: str, data: bytes) -> dict:
        self._check_token()
        url = f"{GRAPH_URL}/{endpoint}"
        try:
            response = self.session.put(
                url=url,
                data=data,
                headers={**dict(self.session.headers), "Content-Type": "application/octet-stream"},
                timeout=30
            )
            response.raise_for_status()
            return handle_response(response)
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            return handle_error(endpoint, e)

    def patch(self, endpoint: str, data: dict) -> dict:
        self._check_token()
        url = f"{GRAPH_URL}/{endpoint}"
        try:
            response = self.session.patch(url=url, json=data, timeout=30)
            response.raise_for_status()
            return handle_response(response)
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            return handle_error(endpoint, e)