import json
from widget_model import WidgetModel
import logging


class TaskManagerConfigModel:

    api_configs = {}

    # Convert the model data into a json file
    @staticmethod
    def to_json():
        master_dict = {"api_configs": {}}
        for api_config_key in TaskManagerConfigModel.api_configs:
            master_dict["api_configs"][api_config_key] = TaskManagerConfigModel.api_configs[api_config_key]

        return json.dumps(master_dict)

    # Pass in a json string to save the config model
    @staticmethod
    def import_json(json_input):
        dict_obj = json.loads(json_input)
        try:
            for api_config in dict_obj["api_configs"].items():
                TaskManagerConfigModel.api_configs[api_config[0]] = api_config[1]
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


    @staticmethod
    def init_default_values():
        saved_widgets_array = None

