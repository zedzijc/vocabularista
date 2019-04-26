
class Translation(object):

    def __init__(self, native_word, foreign_word, score=0):
        self.foreign_word = foreign_word
        self.native_word = native_word
        self.score = score

    def get_foreign_word(self):
        return self.foreign_word

    def get_native_word(self):
        return self.native_word

    def get_score(self):
        return self.score

    def update_score(self, score_delta):
        if self.score + score_delta < 0:
            self.score = 0
        else:
            self.score += score_delta
