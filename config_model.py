import json
from widget_model import WidgetModel
from constants import Constants
from util import get_logging
from pathlib import Path
import logging


class ConfigStore:

    api_configs = {}
    config_log = None

    @staticmethod
    def startup():
        ConfigStore.config_log = get_logging("config_log", logging.DEBUG)
        regenerate_file = False
        config_file = None

        if Constants.CONFIG_FILE_PATH.exists():
            config_file = Constants.CONFIG_FILE_PATH.open(mode='r')

            try:
                config_success = ConfigStore.import_json(config_file.read())
            except json.JSONDecodeError:
                config_success = False

            if config_success:
                ConfigStore.config_log.debug("Successfully loaded config file")
            else:
                ConfigStore.config_log.error("Failed to load config file. Regenerating")
                regenerate_file = True

            config_file.close()
        else:
            regenerate_file = True

        if regenerate_file:
            ConfigStore.config_log.debug("Regenerating config file")
            config_path = Path('.', 'config')
            if not config_path.exists():
                config_path.mkdir()
            config_file = Constants.CONFIG_FILE_PATH.open('w')
            config_file.write(ConfigStore.generate_default_json())
            ConfigStore.init_default_values()
            config_file.close()

        return True

    # Convert the model data into a json file
    @staticmethod
    def to_json():
        master_dict = {"api_configs": {}}
        for api_config_key in ConfigStore.api_configs:
            master_dict["api_configs"][api_config_key] = ConfigStore.api_configs[api_config_key]

        return json.dumps(master_dict)

    # Pass in a json string to save the config model
    @staticmethod
    def import_json(json_input):
        dict_obj = json.loads(json_input)
        try:
            for api_config in dict_obj["api_configs"].items():
                ConfigStore.api_configs[api_config[0]] = api_config[1]
        except KeyError:
            logging.error("Failed to load configuration file")
            return None
        except AttributeError:
            logging.error("Failed to load configuration file")
            return None
        return True

    @staticmethod
    def generate_default_json():
        return '''{
    "api_configs": {}
        }'''

    # Replaces an api with a new dictionary
    @staticmethod
    def update_api(api_name : str, api_config : dict):
        if not api_name in ConfigStore.api_configs:
            return False
            
        ConfigStore.api_configs[api_name] = api_config
        ConfigStore.save_to_file()
        return True

    # Finds if an api config exists
    @staticmethod
    def find_api(api_name : str):
        return api_name in ConfigStore.api_configs

    # Gets the dict object of an api
    @staticmethod
    def get_api(api_name : str) -> dict:
        if (ConfigStore.find_api(api_name)):
            return ConfigStore.api_configs[api_name]
        else:
            return None

    # Adds a new api
    # Replaces an api if it already exists
    @staticmethod
    def add_api(api_name : str, api_config : dict):
        ConfigStore.api_configs[api_name] = api_config
        ConfigStore.save_to_file()
        return True

    @staticmethod
    def init_default_values():
        saved_widgets_array = None

    @staticmethod
    def save_to_file():
        config_file = Constants.CONFIG_FILE_PATH.open(mode='w')
        config_file.write(ConfigStore.to_json())
        config_file.close()

