import json
import logging

logger = logging.getLogger()
logger.setLevel('INFO')


class Configuration:
    def __init__(self, path_json: str) -> None:
        self.settings_path = path_json

    def write_settings(self, settings: dict) -> None:
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(settings, f)
            logging.info(' Settings saved')
        except Exception as err:
            logging.warning(f' Settings are not saved\nError: {err}')
            raise

    def load_settings(self) -> dict:
        settings = None
        try:
            with open(self.settings_path) as f:
                settings = json.load(f)
            logging.info(' Settings are loaded')
        except OSError as err:
            logging.warning(f' Settings are not loaded\nError:{err}')
            raise
        return settings
