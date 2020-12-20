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
    def __init__(self, api_name=None, command=None, username=None, password=None):
        self.api_name = api_name
        self.command = command
        self.username = username
        self.password = password

    def __repr__(self):
        return "api: %s, command: %s, goal: %s, timeframe: %s" % \
               (self.api_name, self.command, self.goal_label, self.time_range)

    def __str__(self):
        return "api: %s, command: %s, goal: %s, timeframe: %s" % \
               (self.api_name, self.command, self.goal_label, self.time_range)

    print("Command object initialized")


class CommandMessageNike(CommandMessage):

    def __init__(self, api_name=None,
                 command=None, graph_type=None,
                 data_type=None, username=None, password=None,
                 goal_miles_total=None, goal_calories_total=None,
                 goal_miles_week=None, goal_miles_month=None,
                 goal_calories_week=None, goal_calories_month=None):

        super().__init__(api_name, command, username, password)

        self.api_name = api_name
        self.command = command
        self.graph_type = graph_type
        self.data_type = data_type
        self.username = username
        self.password = password
        self.goal_miles_total = goal_miles_total
        self.goal_calories_total = goal_calories_total
        self.goal_miles_week = goal_miles_week
        self.goal_calories_week = goal_calories_week
        self.goal_miles_month = goal_miles_month
        self.goal_calories_month = goal_calories_month


class CommandMessageGW:

    def __init__(self, api_name=None,
                 command=None, graph_type=None,
                 data_type=None, username=None, password=None,
                 coordinate_lat=None, coordinate_long=None):

        super().__init__(api_name, command, username, password)

        self.api_name = api_name
        self.command = command
        self.graph_type = graph_type
        self.data_type = data_type
        self.username = username
        self.password = password
        self.coordinate_lat = coordinate_lat
        self.coordinate_long = coordinate_long


class CommandMessageTimeular:

    def __init__(self, api_name=None, command=None,
                 username=None, password=None,
                 time_range=None, goal_label=None,
                 goal_progress=None, goal_wanted=None):

        super().__init__(api_name, command, username, password)

        self.api_name = api_name
        self.command = command
        self.username = username
        self.password = password
        self.time_range = time_range
        self.goal_label = goal_label
        self.goal_progress = goal_progress
        self.goal_wanted = goal_wanted


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
