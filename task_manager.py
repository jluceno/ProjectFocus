from config_model import TaskManagerConfigModel
from os import path
from constants import Constants
from config_main import MainWindow
import logging

class TaskManager:

    started = False
    interface_class = None
    display_class = None
    poll_interval_ms = 0
    config = None

    # Lock to modify the configuration
    config_lock = None

    def __init__(self):
        pass

    # Main function of task manager
    @staticmethod
    def start(self):
        # Startup configure interface

        # Register any functions for the configuration interface

        # Load previous configuration or start a new one
        config = TaskManagerConfigModel()

        regenerate_file = False
        config_file = None

        if path.exists(Constants.CONFIG_FILE_PATH):
            config_file = open(Constants.CONFIG_FILE_PATH, "r")
            config_success = config.import_json(config_file.read())

            if config_success:
                logging.debug("Successfully loaded config file")
            else:
                logging.debug("Failed to load config file. Regenerating")
                regenerate_file = True

            config_file.close()

        if regenerate_file:
            config_file = open(Constants.CONFIG_FILE_PATH, "w")
            config_file.write(TaskManagerConfigModel.generate_default_json())
            config.init_default_values()
            config_file.close()

        # Startup display class
        TaskManager.display_class = MainWindow()

        # Setup the display
        TaskManager.display_class.config()
        TaskManager.display_class.register_command_func(TaskManager._command_function())

        pass

    # Adds a new configuration
    @staticmethod
    def add_widget_config(config_command):
        # Pause the polling thread

        # Update the configuration

        # Get data from the API for the new object

        # Resume the polling thread

        pass

    # Removes a configuration
    @staticmethod
    def remove_widget_config(config_command):
        # Pause the polling thread

        # Remove the config

        # Resume the polling thread
        pass

    # Gets the whole configuration of the application
    # Helps preview the current state of the display to the configuration
    @staticmethod
    def get_current_configuration():
        # Read and return the current configuration

        # Must remove all authentication data

        pass

    @staticmethod
    def _command_function(command):
        pass
