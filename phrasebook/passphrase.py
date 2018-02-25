import os

from Crypto.Random import random


class Wordlist:
    """
    Holds details about the current wordlist.
    """
    words = None

    def __init__(self, path=None):
        """
        Parse either a provided file or a default.

        Args:
        path -- if provided, uses the custom wordlist at path
        """
        if not path:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'wordlists',
                                'en.txt')

        with open(path) as f:
            self.words = f.read().splitlines()

    @classmethod
    def for_locale(cls, locale):
        """
        Returns a new Wordlist object using the default wordlist for that
        locale, or the en wordlist as a default.
        """
        if locale != 'en':
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'wordlists',
                                locale + '.txt')
            if os.path.exists(path):
                return cls(path)
            else:
                return cls()

    def gen_passphrase(self, num):
        """
        Generates a passphrase from the wordlist.

        Args:
        num -- number of words to use in the wordlist.
        """
        return ' '.join(random.choice(self.words)
                        for x in range(num))
