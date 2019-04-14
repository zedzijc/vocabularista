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
