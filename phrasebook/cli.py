import sys

import click
from locale import getlocale

from phrasebook.gui import PhraseWindow, app
from phrasebook.wordlist import get_supported_locales


@click.command()
@click.option("-w", "--word-list",
              help="Path to a file with a list of words to choose from, separated by newlines",
              type=click.Path(exists=True))
@click.option("-n", "--num-words",
              help="Number of words to include in the passphrase (must be between 4 and 15)",
              type=click.IntRange(4, 15),
              default=6)
@click.option("-l", "--locale",
              help="The locale to use when selecting a wordlist.",
              type=click.Choice(get_supported_locales()))
def main(word_list=None, num_words=None, locale=None):
    """
    Entry point for CLI.
    """
    if not locale:
        locale = getlocale()[0]

    phrase_win = PhraseWindow(
        word_list_path=word_list,
        num_words=num_words,
        locale=locale,
    )
    phrase_win.show()
    sys.exit(app.exec_())
