import json
from widget_model import WidgetModel


class TaskManagerConfigModel:

    saved_widgets_array = None

    # Convert the model data into a json file
    def to_json(self):
        json_saved_widgets_array = []
        for widget in json_saved_widgets_array:
            json_saved_widgets_array.append(widget.to_json_map())
        return json.dumps(json_saved_widgets_array)

    # Pass in a json string to save the config model
    def import_json(self, json_input):
        return True

    @staticmethod
    def generate_default_json():
        return "test"

    def init_default_values(self):
        saved_widgets_array = None

