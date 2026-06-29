import logging
from pathlib import Path
from datetime import datetime

def setup_logger(base_dir: Path):
    now = datetime.now()
    log_dir = base_dir / "logs"

    file_name = log_dir / f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.log"

    logging.basicConfig(
        format='%(asctime)s %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler(file_name),
        ]
    )

    return logging.getLogger(__name__)

if __name__ == "__main__":
    path = Path(__file__).parent.parent.parent
    print(path)
    setup_logger(path)

    logger = logging.getLogger(__name__)
    logger.info("teste")