import json
import logging


def load_settings(path_json: str) -> dict:
    settings = None
    try:
        with open(path_json) as f:
            settings = json.load(f)
        logging.info(' Settings are loaded')
    except OSError as err:
        logging.warning(
            f' Settings are not loaded\nError:{err}')
        raise
    return settings
