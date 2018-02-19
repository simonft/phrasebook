import sys

from phrasebook.gui import PhraseWindow, app


def main():
    phraseWin = PhraseWindow()
    phraseWin.show()
    sys.exit(app.exec_())
