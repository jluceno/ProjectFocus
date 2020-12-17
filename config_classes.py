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

    def __init__(self, api_name=None,
                 command=None, graph_type=None,
                 data_type=None, username=None, password=None):

        self.api_name = api_name
        self.command = command
        self.graph_type = graph_type
        self.data_type = data_type
        self.username = username
        self.password = password

        print("Command object initialized")


class CommandMessageNike(CommandMessage):

    def __init__(self, api_name=None, command=None, graph_type=None, data_type=None,
                 username=None, password=None, goal_miles=None, goal_calories=None):

        super().__init__(api_name, command, graph_type,
                         data_type, username, password)

        self.goal_miles = goal_miles
        self.goal_calories = goal_calories

    def __repr__(self):
        return "api: %s, command: %s, graph type: %s" % (self.api_name, self.command, self.graph_type)

    def __str__(self):
        return "api: %s, command: %s, graph type: %s" % (self.api_name, self.command, self.graph_type)


class CommandMessageGW(CommandMessage):

    def __init__(self, api_name=None, command=None, graph_type=None,
                 data_type=None, username=None, password=None,
                 coordinate_lat=None, coordinate_long=None):

        super().__init__(api_name, command, graph_type,
                         data_type, username, password)

        self.coordinate_lat = coordinate_lat
        self.coordinate_long = coordinate_long

    def __repr__(self):
        return "api: %ds, command: %ds, graph type: %ds" % (self.api_name, self.command, self.graph_type)

    def __str__(self):
        return "api: %ds, command: %ds, graph type: %ds" % (self.api_name, self.command, self.graph_type)


class CommandType(enum.Enum):
    add = 1
    remove = -1

# TaskManager =====================================
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
# Do nike stuff
