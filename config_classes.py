import enum


# declare enums to select from (goal or uncontrollable)
# api_enum = nike, something, etc.
# commands = add, remove
# graph_type = progress_bar, display_value
#   optional params:
#      for progress_bar:
#      int max_goal


# pycharm asks for CamelClass
class CommandMessage:

    def __init__(self, api_name,
                 command, graph_type,
                 data_type):

        self.api_name = api_name
        self.command = command
        self.graph_type = graph_type
        self.data_type = data_type

        print("command message received\n")
        print(api_name)


# keep


class Command(enum.Enum):
    add = 1
    remove = -1
    # tentative optional parameters class
    # class Params:
