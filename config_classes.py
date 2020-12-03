import enum


# pycharm asks for CamelClass
class CommandWidget(enum.Enum):
    def __init__(self, api_name):
        self.api_name = api_name

    # members for enum implementation
    add = 55
    remove = 66
    edit = 77

    def add_widget(self):
        print(self.add)

    def remove_widget(self):
        print(self.remove)

    def edit_widget(self):
        print(self.edit)


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




