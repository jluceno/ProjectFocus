import enum


# declare enums to select from (goal or uncontrollable)
# api_enum = nike, something, etc.
# commands = add, remove
# graph_type = progress_bar, display_value
#   optional params:
#      for progress_bar:
#      int max_goal


# Nike: CommandMessageNike class inherit for specifics - calories, miles

# pycharm asks for CamelClass
class CommandMessage:

# ADD USERNAME, PASSWORD

    def __init__(self, api_name,
                 command, graph_type,
                 data_type, username, password):

        self.api_name = api_name
        self.command = command
        self.graph_type = graph_type
        self.data_type = data_type
        self.username = username
        self.password = password

        print("Command object initialized")
        print(api_name)


class CommandMessageNike(CommandMessage):

    def __init__(self, goal_miles, goal_calories):
        self.goal_miles = goal_miles
        self.goal_calories = goal_calories


class CommandMessageGW(CommandMessage):

    def __init__(self, coordinates):
        self.coordinates = coordinates


# keep


class CommandType(enum.Enum):
    add = 1
    remove = -1
    # tentative optional parameters class
    # class Params:




# Taskmanager =====================================
#
# def getCommand(cmd):
#     incoming_command = Command(cmd)
#
#     test = {
#         CommandType.add: TaskManager.call_add()
#     }
#
#     test.get(incoming_command.command_type)
#
#     test2 = {
#         "add": TaskManager.call_add()
#     }
#
#     test2.get(cmd["command_type"])
#
#
#     # Figure out which API to call
#     if cmd["api"] is "Nike":
#         pass
#         # Do nike stuff