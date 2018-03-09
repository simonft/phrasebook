import os
from pkg_resources import resource_exists, resource_string

from random import SystemRandom


class Wordlist:
    """
    Holds details about the current wordlist.
    """
    words = None

    def __init__(self, words):
        """
        Args:
        word -- an array of words
        """
        self.words = words

    @classmethod
    def for_locale(cls, locale=None):
        """
        Returns a new Wordlist object using the default wordlist for that
        locale, or the en wordlist as a default.
        """
        resource = None
        if locale:
            resource_path = 'wordlists/' + locale + '.txt'
            if resource_exists('phrasebook', resource_path):
                resource = 'wordlists/' + locale + '.txt'
        if not resource:
            resource = 'wordlists/en.txt'

        wordlist = resource_string('phrasebook', resource).decode('utf-8')

        return cls(wordlist.splitlines())

    @classmethod
    def open_path(cls, path):
        """
        Parse either a provided file. Throws FileTooLargeExeception
        if the file is over 5mb, or BadWordlistException if there's something wrong
        with the contents of the wordlist.

        Args:
        path -- a string the path to the wordlist to open
        """
        # Make sure the file isn't over 5 megabytes in size. This is
        # an arbitrarily chosen "too large to be reasonable".
        if os.stat(path).st_size > 1024 * 1024 * 5:
            raise FileTooLargeExeception()

        with open(path) as f:
            words = f.read().splitlines()

        Wordlist.sanity_check_wordlist(words)
        return cls(words)

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

