from language import Translation
from command_line import CommandLineInputSection, CommandLineActivity


class Session(object):

    def __init__(self, database):
        self.database = database
        self.user_input = []

    def _get_last_user_input(self):
        return self.user_input[-1] if self.user_input else None


class AddTranslationsSession(Session):

    def __init__(self, database):
        self.add_translation_activity = CommandLineInputSection([
            CommandLineActivity(
                self.cancel_session, "Quit"),
            CommandLineActivity(
                self.edit_last_translation, "Edit previous translation")],
            "Add translations")
        self.edit_translation_activity = CommandLineInputSection(
            [CommandLineActivity(
                self.cancel_session, "Quit")],
            "Edit translation")
        super().__init__(database)

    def cancel_session(self):
        return -1

    def _prompt_native_word(self, activity, prompt):
        return activity.run(prompt)

    def _prompt_foreign_word(self, activity, prompt):
        return activity.run(prompt)

    def _save_translations(self):
        for translation in self.user_input:
            self.database.add_translation(translation.get_native_word(),
                                          translation.get_foreign_word())
        for item in self.user_input:
            print(item.get_native_word(), item.get_foreign_word())
        #self.database.commit_changes()

    def edit_last_translation(self):
        last_translation = self._get_last_user_input()
        edited_last_translation = self._prompt_translation(
                                    self.edit_translation_activity,
                                    last_translation.get_native_word(),
                                    last_translation.get_foreign_word())
        if edited_last_translation:
            self.user_input[-1] = edited_last_translation

    def _prompt_translation(self, activity, native_prompt, foreign_prompt):
        native_word = self._prompt_native_word(activity, native_prompt)
        if native_word == -1 or not native_word:
            return None
        foreign_word = self._prompt_foreign_word(activity, foreign_prompt)
        if foreign_word == -1 or not foreign_word:
            return None
        return Translation(native_word, foreign_word)

    def start(self):
        while True:
            translation = self._prompt_translation(
                            self.add_translation_activity,
                            "Enter native word",
                            "Enter foreign word")
            if translation:
                self.user_input.append(translation)
            else:
                break
        self._save_translations()
