from config_model import TaskManagerConfigModel
from os import path
from constants import Constants
import logging

class TaskManager:

    interface_class = None
    display_class = None
    poll_interval_ms = 0
    config = None

    # Lock to modify the configuration
    config_lock = None

    def __init__(self):
        pass

    # Main function of task manager
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

        # Setup the display

        # Run the polling thread

        pass

    # Causes the task manager to update
    def _update(self):
        pass

    # Thread that will poll data APIs
    def _poll_thread(self):
        # Iterate through all widgets and update them

        pass

    # Adds a new configuration
    def add_widget_config(self, config_command):
        # Pause the polling thread

        # Update the configuration

        # Get data from the API for the new object

        # Resume the polling thread

        pass

    # Removes a configuration
    def remove_widget_config(self, config_command):
        # Pause the polling thread

        # Remove the config

        # Resume the polling thread
        pass

    # Gets the whole configuration of the application
    # Helps preview the current state of the display to the configuration
    def get_current_configuration(self):
        # Read and return the current configuration

        # Must remove all authentication data

        pass
