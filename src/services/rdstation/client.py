import logging
import requests
import time
from src.settings.config import Settings
from datetime import datetime

logger = logging.getLogger(__name__)


class RdClient:
    def __init__(self, settings: Settings):
        self.url = settings.rd_api_url
        self.token = settings.rd_api_token

        self.session = requests.Session()
        self.session.headers.update({"accept": "application/json"})

        self.limit_per_minute = 120
        self.count_request = 0
        self.window_start = datetime.now()

    def _check_rate_limit(self):
        elapsed = (datetime.now() - self.window_start).total_seconds()

        if elapsed >= 60:
            self.count_request = 0
            self.window_start = datetime.now()
            return

        if self.count_request >= self.limit_per_minute:
            wait_time = 60 - elapsed
            logger.info(f"Rate limit atingido, aguardando {wait_time}s")
            time.sleep(wait_time)
            self.count_request = 0
            self.window_start = datetime.now()

    def get(self, endpoint: str, params: dict = None) -> dict:
        self._check_rate_limit()
        self.count_request += 1

        if params is None:
            params = {}

        params["token"] = self.token
        url = f"{self.url}/{endpoint}"

        try:
            response = self.session.get(url=url, params=params)
            response.raise_for_status()

            body = response.json()
            is_list = isinstance(body, list)

            data = body if is_list else body.get(endpoint, [])

            return {
                "status": "success",
                "total": len(data) if is_list else body.get("total", 0),
                "has_more": False if is_list else body.get("has_more", False),
                "next_page": None if is_list else body.get("next_page", None),
                "data": data
            }
        except requests.exceptions.HTTPError as e:
            logger.error(f"[{endpoint}] HTTP error: {e}")
            return {"status": "erro", "total": 0, "has_more": False, "data": [], "message": str(e)}
        except requests.exceptions.RequestException as e:
            logger.error(f"[{endpoint}] Request error: {e}")
            return {"status": "erro", "total": 0, "has_more": False, "data": [], "message": str(e)}