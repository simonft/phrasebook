import os
from pkg_resources import resource_string
from random import SystemRandom

from babel import parse_locale, get_locale_identifier


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
    def for_locale(cls, locale="en"):
        """
        Returns a new Wordlist object using an included wordlist most
        appropriate to the provided locale, or the en wordlist as a default.

        This parses the locale string and first tries to find a file matching
        both the language and territory. Failing that, it tries to find one
        matching the language. Failing that, it falls back to `en`.

        Args:
        locale -- An RFC 4646 locale string (optional)
        """
        wordlist_path_string = "wordlists/{}.txt".format
        if locale:
            locale_tuple = parse_locale(locale)
            for test_wordlist_locale in [locale_tuple[:2], locale_tuple[:1], "en"]:
                path = wordlist_path_string(get_locale_identifier(test_wordlist_locale))
                try:
                    return cls(resource_string('phrasebook', path).decode('utf-8').splitlines())
                except FileNotFoundError:
                    continue

        # This should never happen, since the "en" file should always be there
        # as a fallback. If for some reason it's not, exit with a helpful
        # exception message.
        raise Exception("No suitable wordlist file found")

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

