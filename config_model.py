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
    mm_config_start_pos = 0
    mm_config_var_length = 0
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
            pattern = re.compile('(?<=var config =)([\s\S]*?);')
            matches = pattern.search(mm_config_data)
            match = matches.group(1)
            ConfigStore.mm_config_start_pos = matches.start()
            ConfigStore.mm_config_var_length = len(match)
            ConfigStore.mm_config = demjson.decode(match)
            
        except:
            mm_config_file.close()
            ConfigStore.config_log.debug("Failed to load the mm config")
            return False

        ConfigStore.config_log.debug("Loaded the mm config")
        return True

    # Writes the magic mirror config
    @staticmethod
    def export_mm_config():
        mm_config_file = Constants.MM_CONFIG_FILE_PATH.open("r")
        mm_config_data = mm_config_file.read()
        mm_config_file.close()

        mm_config_data = (
           mm_config_data[:ConfigStore.mm_config_start_pos]
         + json.dumps(ConfigStore.mm_config)
         + mm_config_data[ConfigStore.mm_config_start_pos + ConfigStore.mm_config_var_length:]
        )

        mm_config_file = Constants.MM_CONFIG_FILE_PATH.open("w")
        mm_config_file.write(mm_config_data)
        mm_config_file.close()

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
        if api_name is "Nike":
            ConfigStore.api_configs[api_name] = api_config
            ConfigStore.save_to_file()
        elif api_name is "Weather":
            ConfigStore.configure_weather((api_config[0], api_config[1]))
        else:
            return False
        return True

    @staticmethod
    def init_default_values():
        saved_widgets_array = None

    @staticmethod
    def save_to_file():
        config_file = Constants.CONFIG_FILE_PATH.open(mode='w')
        config_file.write(ConfigStore.to_json())
        config_file.close()

    @staticmethod
    def configure_weather(weather_config_tuple : tuple):
        
        found_weather = False
        weather_index = 0
        configured_map = {
                    'module': 'weather',
                    'position': 'top_center',
                    'config': 
                    {
                        'weatherProvider': 'openweathermap',
                        'type': 'current',
                        'apiKey': weather_config_tuple[0],
                        'location': weather_config_tuple[1]
                    }
                }

        for idx, module_config in enumerate(ConfigStore.mm_config['modules']):
            if module_config['module'] == 'weather':
                found_weather = True
                weather_index = idx
        
        # If config entry does not exist
        if not found_weather:
            ConfigStore.mm_config['modules'].append(configured_map)

        # If config entry does exist
        else:
            ConfigStore.mm_config['modules'][weather_index] = configured_map

        ConfigStore.export_mm_config()