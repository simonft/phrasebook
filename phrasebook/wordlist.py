import os

from random import SystemRandom


class Wordlist:
    """
    Holds details about the current wordlist.
    """
    words = None

    def __init__(self, path=None):
        """
        Parse either a provided file or a default. Throws FileTooLargeExeception
        if the file is over 5mb, or BadWordlistException if there's something wrong
        with the contents of the wordlist.

        Args:
        path -- if provided, uses the custom wordlist at path
        """
        if not path:
            path = os.path.join(os.path.dirname(__file__), 'wordlists', 'en.txt')

        # Make sure the file isn't over 5 megabytes in size. This is
        # an arbitrarily chosen "too large to be reasonable".
        if os.stat(path).st_size > 1024 * 1024 * 5:
            raise FileTooLargeExeception()

        with open(path) as f:
            self.words = f.read().splitlines()

        self.sanity_check_wordlist(self.words)

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
        random = SystemRandom()
        return ' '.join(random.choice(self.words)
                        for x in range(num))

    @staticmethod
    def sanity_check_wordlist(words):
        """
        Runs a few sanity checks on the wordlist

        Args:
        words -- an array containing a list of words
        """
        if len(words) != len(dict.fromkeys(words)):
            raise FileHasDuplicateLinesException()

        for word in words:
            if word == "":
                raise WordIsBlankException()
            if " " in word:
                raise WordHasSpaceExecption()
            if len(word) >= 20:
                raise WordTooLongException()


class FileTooLargeExeception(Exception):
    """Thrown when a file is unreasonably large to read in"""
    pass


class BadWordlistException(Exception):
    """Base class for a word list that has problems with it's format or contents"""
    pass


class FileHasDuplicateLinesException(BadWordlistException):
    """Thrown when two or more lines of a file are the same"""
    pass


class WordHasSpaceExecption(BadWordlistException):
    """Thrown when a line has a space in it"""
    pass


class WordTooLongException(BadWordlistException):
    """Thrown when a word is unreasonably long"""
    pass


class WordIsBlankException(BadWordlistException):
    """Thrown when a word is unreasonably long"""
    pass

