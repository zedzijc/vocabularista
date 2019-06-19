from database import DatabaseHandler
from command_line import MenuSection, CommandLineActivity
from session import AddTranslationsSession
import sys


class Controller(object):

    def __init__(self):
        self.database = DatabaseHandler()
        self.main_menu = self._init_main_menu()
        self._run_menu(self.main_menu)

    def _init_main_menu(self):
        main_menu = MenuSection([
            CommandLineActivity(
                self.quit,
                "Quit"),
            CommandLineActivity(
                self.run_add_translations,
                "Add translations"),
            CommandLineActivity(
                self.run_pracice_session,
                "Practice")
            ],
            "Main menu")
        return main_menu

    def _run_menu(self, menu):
        while True:
            menu.run()

    def run_add_translations(self):
        session = AddTranslationsSession(self.database)
        session.start()

    def run_pracice_session(self):
        print("run practice session")

    def previous_translation(self):
        print("run previous translation")

    def quit(self):
        print("quitting safely")
        sys.exit(0)
