import json
from widget_model import WidgetModel
from constants import Constants
from util import get_logging
from pathlib import Path
import logging
import re
import demjson


class ConfigStore:

    api_configs = {}
    mm_config = None
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

        if not ConfigStore.import_mm_config():
            return False

        return True

    # Convert the model data into a json file
    @staticmethod
    def to_json():
        master_dict = {"api_configs": {}}
        for api_config_key in ConfigStore.api_configs:
            master_dict["api_configs"][api_config_key] = ConfigStore.api_configs[api_config_key]

        return json.dumps(master_dict)

    # Loads the magic mirror config into a var
    @staticmethod
    def import_mm_config():
        ConfigStore.config_log.debug("Loading the mm config")
        try:
            mm_config_file = Constants.MM_CONFIG_FILE_PATH.open("r")
            mm_config_data = mm_config_file.read()

            # Save the config var from the javascript config file
            pattern = re.compile('(?<=var config =)([\s\S]*?)(;)')
            parsed = pattern.findall(mm_config_data)
            ConfigStore.mm_config = demjson.decode(parsed[0][0])
        except:
            mm_config_file.close()
            ConfigStore.config_log.debug("Failed to load the mm config")
            return False

        ConfigStore.config_log.debug("Loaded the mm config")
        return True

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

