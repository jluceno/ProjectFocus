import enum


# declare enums to select from (goal or uncontrollable)
# api_enum = nike, something, etc.
# commands_enum = add, remove, edit
# graph_type_enum = bar, pie, line, display_value

# pycharm asks for CamelClass
class CommandMessage:
    def __init__(self, api_name):
        self.api_name = api_name

    class ApiEnum(enum.Enum):
        nike = 1
        samsung = 2
        google_weather = 3

    class GraphType(enum.Enum):
        bar = 1
        line = 2
        pie = 3
        simple = 4

    class Command(enum.Enum):
        add = 1
        remove = 2


class Goal:
    def __init__(self, graph_type, goal_value, goal_type):

        # bar, line, pie graph
        self.graph_type = graph_type

        # value of goal
        self.goal_value = goal_value

        # daily, weekly, monthly goal
        self.goal_type = goal_type


class Uncontrollable:
    def __init__(self, value):

        # could be temperature, humidity, date
        self.value = value




