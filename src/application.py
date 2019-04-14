from database import DatabaseHandler
from vocabulary import Vocabulary
from language import Translation
from command_line import CommandLineInterface
import random


class Application(object):

    def __init__(self):
        self.db_handler = DatabaseHandler()
        self.cli = CommandLineInterface()

    def run(self):
        #  database.perform_initial_setup()
        quit = False
        while not quit:
            activity = self.cli.main_menu()

            if activity == "Translate":
                self.log_translations()

            elif activity == "Practice":
                self.practice()

            quit = activity == "quit"

        #  save here
        print("Saved your progress. Good work, have a great day!")

    def log_translations(self):
        print("\nTo exit, leave one or more fields empty.\n")
        while True:
            translation = self.cli.register_translation()
            native_word = translation[0]
            foreign_word = translation[1]
            if not (native_word and foreign_word):
                break
            self.db_handler.add_translation(native_word, foreign_word)
            print("\n Added translation!\n\n")
            print("-------------------------")

    def practice(self):
        translations = self.load_translations()
        print("\nTo exit, leave answer empty.\n")
        while True:
            translation = self.get_random_translation(translations)
            answer = self.cli.translate(translation.get_foreign_word())
            if not answer:
                if self.cli.verify_quit() == "yes" or "1" or "quit" or "exit":
                    break
            if answer.lower() == translation.get_native_word().lower():
                score_change = 1
                print("\nCorrect!\n")
            else:
                print("\nWrong, correct answer: {0}\n".format(
                    translation.get_foreign_word()))
                score_change = -2
            self.update_difficulty(translations, translation, score_change)

    def load_translations(self):
        translations = {"hard": [], "medium": [], "easy": []}
        for db_translation in self.db_handler.load_translations():
            score = db_translation[2]
            translations[self.get_difficulty(score)].append(
                Translation(db_translation[0], db_translation[1], score))
        return translations

    def get_random_translation(self, translations):
        while True:
            translation_list = translations[self.random_difficulty()]
            if translation_list:
                return random.choice(translation_list)

    def get_difficulty(self, score):
        difficulty = "hard"
        if score > 10:
            if score < 20:
                difficulty = "medium"
            else:
                difficulty = "easy"
        return difficulty

    def random_difficulty(self):
        difficulty = random.randint(1, 101)
        if difficulty < 46:
            return "hard"
        elif difficulty < 81:
            return "medium"
        return "easy"

    def update_difficulty(self, translations, translation, score_delta):
        score = translation.get_score()
        previous_difficulty = self.get_difficulty(score)
        difficulty = self.get_difficulty(score + score_delta)
        translation.update_score(score_delta)
        if difficulty != previous_difficulty:
            translations[previous_difficulty].remove(translation)
            translations[difficulty].append(translation)


if __name__ == '__main__':
    app = Application()
    app.run()
