import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(name)s %(message)s %(asctime)s',
    datefmt='%Y-%m-%dT%H:%M'
)


def get_logger(name: str):
    return logging.getLogger(name)
