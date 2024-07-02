# logging_config.py
import logging


def setup_logging():
    logging.basicConfig(level=logging.INFo, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


setup_logging()
