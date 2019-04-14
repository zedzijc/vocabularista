import sqlite3


class DatabaseHandler(object):

    def __init__(self):
        self.db = sqlite3.connect("database/db")
        self.cursor = self.db.cursor()

    def commit_changes(self):
        self.db.commit()

    def load_data(self, command):
        self.cursor.execute(command)
        return self.cursor.fetchall()

    def perform_initial_setup(self):
        self.cursor.execute("CREATE TABLE native_words \
                            (content TEXT PRIMARY KEY);")
        self.cursor.execute("CREATE TABLE foreign_words \
                            (content TEXT NOT NULL);")
        self.cursor.execute("CREATE TABLE translations \
                            (native_word INTEGER, \
                            foreign_word INTEGER, \
                            score INTEGER, \
                            FOREIGN KEY (native_word) \
                               REFERENCES native_words(content), \
                            FOREIGN KEY (foreign_word) \
                                REFERENCES foreign_words(content), \
                            PRIMARY KEY (native_word, \
                                        foreign_word));")

    def add_native_word(self, word):
        self.cursor.execute("INSERT OR IGNORE INTO native_words \
                            (content) VALUES (?);", (word,))

    def add_foreign_word(self, word):
        self.cursor.execute("INSERT OR IGNORE INTO foreign_words \
                            (content) VALUES (?);", (word,))

    def add_translation(self, native_word, foreign_word, score=0):
        self.cursor.execute("INSERT OR IGNORE INTO translations \
                            (native_word, foreign_word, score) \
                            VALUES (?, ?, ?);",
                            (native_word, foreign_word, score))

    def update_native_word(self, word):
        self.cursor.execute("UPDATE native_words SET content = ? \
                            WHERE content = ?;", (word, word))

    def update_foreign_word(self, word):
        self.cursor.execute("UPDATE foreign_words SET content = ? \
                            WHERE content = ?;", (word, word))

    def update_translation_score(self, native_word, foreign_word, score):
        self.cursor.execute("UPDATE translations SET score = ? \
                            WHERE native_word = ? \
                            AND foreign_word = ?;",
                            (score, native_word, foreign_word))

    def delete_translation(self, native_word, foreign_word):
        self.cursor.execute("DELETE FROM translations \
                            WHERE native_word = ? \
                            AND foreign_word = ?;",
                            (native_word, foreign_word))

    def load_native_words(self):
        return self.load_data("SELECT * FROM native_words;")

    def load_foreign_words(self):
        return self.load_data("SELECT * FROM foreign_words;")

    def load_translations(self):
        return self.load_data("SELECT * FROM translations;")
