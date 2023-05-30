import json
import logging

logger = logging.getLogger()
logger.setLevel('INFO')


class Configuration:
    def write_card(self, card: dict, path_json: str) -> None:
        """Writes the card number in json.
        Args:
            card (dict): Сard number and algorithm Luhn result.
            path_json (str): Path to file.
        """
        settings = Configuration.load_settings(self, path_json)
        d = dict.fromkeys(['card'], card)
        settings.update(d)
        try:
            with open(path_json, 'w') as f:
                json.dump(settings, f)
            logging.info(' Card saved')
        except Exception as err:
            logging.warning(f' Card are not saved\nError: {err}')
            raise

    def load_settings(self, path_json: str) -> dict:
        """Loads settings from json.
        Args:
            path_json (str): Path to file.
        Returns:
            dict: Settings.
        """
        settings = None
        try:
            with open(path_json) as f:
                settings = json.load(f)
            logging.info(' Settings are loaded')
        except OSError as err:
            logging.warning(f' Settings are not loaded\nError:{err}')
            raise
        return settings
