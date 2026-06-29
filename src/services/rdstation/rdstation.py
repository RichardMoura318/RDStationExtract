import logging
from datetime import datetime, timedelta
from src.services.rdstation.client import RdClient
from src.settings.endpoints import ENDPOINTS_CONFIG

logger = logging.getLogger(__name__)


class RdService:
    def __init__(self, client: RdClient):
        self.client = client

    def get_data(self, endpoint_name: str) -> list[dict]:
        config = ENDPOINTS_CONFIG.get(endpoint_name)

        if not config:
            logger.error(f"Endpoint {endpoint_name} não encontrado no config")
            return []

        if not config["paginated"]:
            logger.info(f"[{endpoint_name}] modo: simples")
            return self._get_simple(endpoint_name)

        if config["period_params"]:
            response = self.client.get(endpoint_name, params={"limit": 1, "page": 1})
            total = response.get("total", 0)

            if total >= 10000:
                logger.info(f"[{endpoint_name}] Total superior a 10k - modo: periodo")
                return self._get_by_period(endpoint_name, config)
            else:
                logger.info(f"[{endpoint_name}] Total inferior a 10k - modo: simples paginado")
                return self._get_by_page(endpoint_name, config)
        else:
            logger.info(f"[{endpoint_name}] modo: paginado")
            return self._get_by_page(endpoint_name, config)

    def _get_simple(self, endpoint_name: str) -> list[dict]:
        response = self.client.get(endpoint_name)

        if response.get("status") != "success":
            logger.error(f"[{endpoint_name}] Erro na coleta: {response.get('message')}")
            return []

        data = response.get("data")

        return data if isinstance(data, list) else []

    def _get_by_page(self, endpoint_name: str, config: dict, extra_params: dict = None) -> list[dict]:
        if extra_params is None:
            extra_params = {}

        all_data = []
        page = 1
        use_next_page = config.get("next_page", False)
        next_page_token = None

        while True:
            params = {"page": page, "limit": 200, **extra_params}

            if use_next_page and next_page_token:
                params["next_page"] = next_page_token

            response = self.client.get(endpoint_name, params=params)

            if response.get("status") != "success":
                logger.error(f"[{endpoint_name}] Erro na coleta: {response.get('message')}")
                break

            data = response.get("data")
            has_more = response.get("has_more")

            if not data:
                break

            all_data.extend(data)

            logger.debug(f"[{endpoint_name}] page={page} - has_more={has_more} - collected={len(all_data)}")

            if not has_more:
                break

            if use_next_page:
                next_page_token = response.get("next_page")
            else:
                page += 1

        return all_data

    def _get_by_period(self, endpoint_name: str, config: dict) -> list[dict]:
        start_date = datetime.today() - timedelta(days=730)
        end_date = datetime.today()
        all_data = []

        while start_date < end_date:
            next_date = min(start_date + timedelta(days=365), end_date)

            logger.info(f"[{endpoint_name}] Coletando periodo: {start_date.date()} a {next_date.date()}")

            params = config["period_params"](start_date, next_date)
            data = self._get_by_page(endpoint_name, config, extra_params=params)
            all_data.extend(data)

            start_date = next_date

        return all_data

if __name__ == "__main__":
    import json
    import logging
    from src.settings.config import Settings

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] - %(message)s",
        datefmt="%d/%m/%y %H:%M:%S"
    )

    settings = Settings()
    rd_client = RdClient(settings=settings)
    service = RdService(client=rd_client)

    endpoints_to_test = ["deal_stages"]

    for endpoint in endpoints_to_test:
        logger.info(f"Testando endpoint: {endpoint}")
        data = service.get_data(endpoint)
        logger.info(f"[{endpoint}] Total coletado: {len(data)}")

        filename = f"{endpoint}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

        logger.info(f"[{endpoint}] Salvo em: {filename}")
        print("-" * 60)