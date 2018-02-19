import os

from Crypto.Random import random


class Wordlist:
    words = None

    def __init__(self, path=None):
        if not path:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'wordlists',
                                'en.txt')
        with open(path) as f:
            self.words = f.read().splitlines()

    @classmethod
    def for_locale(cls, locale):
        if locale != 'en':
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'wordlists',
                                locale + '.txt')
            if os.path.exists(path):
                return cls(path)
            else:
                return cls()

    def gen_passphrase(self, num):
        return ' '.join(random.choice(self.words)
                        for x in range(num))
