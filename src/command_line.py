import sys

"""
class CommandLineInterface(object):

    def main_menu(self):
        activity = input("Choose an activity:\n\
            1) Add new translation \n\
            2) Practice \n\
            *) Exit \n")
        if activity == "1" or "trans" in activity:
            return "Translate"

        elif activity == "2" or "prac" in activity:
            return "Practice"

        return "quit"

    def register_translation(self):
        native_word = input("\n Native_word: \n ")
        foreign_word = input("\n Foreign_word: \n ")
        return (native_word, foreign_word)

    def translate(self, string):
        return input(string + ": \n")

    def verify_quit(self):
        return input("Confirm quitting by typing either 'yes', '1', or 'quit'")
"""


class MenuSection(object):

    def __init__(self, activities, description):
        self.description = description
        self.options = {}
        self._init_options(activities)

    def get_description(self):
        return self.description

    def run(self):
        return self._execute_option(self._prompt())

    def _init_options(self, activities):
        i = 0
        for activity in activities:
            self.options[str(i)] = activity
            i += 1

    def _get_options(self):
        options = ""
        for index, option in self.options.items():
            options += option._get_cli_option_string(index, option) + "\n"
        return options

    def _get_cli_option_string(self, index, command_line_section):
        return "{0}) {1}".format(index, command_line_section.get_description())

    def _prompt(self):
        return input(self._get_options())

    def _execute_option(self, option_index):
        if option_index in self.options:
            return self.options[option_index].run()
        else:
            print("Unknown option chosen: {0}".format(option_index))
        self.run()


class CommandLineActivity(MenuSection):

    def __init__(self, activity, description):
        self.activity = activity
        super().__init__(None, description)

    def _init_options(self, activities):
        pass

    def run(self):
        return self.activity()


class CommandLineInputSection(MenuSection):

    def __init__(self, activities, description=None):
        super().__init__(activities, description)

    def run(self, input_label):
        return self._execute_option(input_label, self._prompt(input_label))

    def _get_options(self, input_label):
        options = ""
        for index, option in self.options.items():
            options += option._get_cli_option_string(index, option) + "\n"
        return options + "\n" + input_label + ": "

    def _prompt(self, input_label):
        return input(self._get_options(input_label))

    def _execute_option(self, input_label, user_input):
        if user_input in self.options:
            verdict = self.options[user_input].run()
            return (verdict if verdict == self.options['0'].run() else
                    self.run(input_label))
        else:
            return user_input
