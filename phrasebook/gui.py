import functools
import math
import os
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon
from babel import Locale

from phrasebook import _
from phrasebook.wordlist import (Wordlist,
                                 FileTooLargeExeception,
                                 BadWordlistException,
                                 get_wordlists_by_locale)


class PhraseWindow(QtWidgets.QMainWindow):
    """The main QT window for the program."""
    def __init__(self, word_list_path=None, num_words=None, locale=None):
        """
        Sets up the main window.

        Keyword arguments:
        word_list_path -- A string containing the path to a custom wordlist
        num_words -- The number of words to display
        locale -- A locale when choosing a default wordlist. Not yet implemented.
        """
        QtWidgets.QMainWindow.__init__(self)

        self.setStyleSheet(
            """
            QMainWindow {
              background-color: #ededed;
            }
            """
        )

        if word_list_path:
            if not self.open_file(word_list_path):
                sys.exit(1)
        else:
            self.wordlist = Wordlist.for_locale(locale)

        # Fits reasonably well on a 1024x768 srceen.
        self.setMinimumSize(QSize(400, 220))
        self.resize(940, 220)
        self.setWindowTitle("Phrasebook")

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.warning_line_widget = WarningLineWidget("")

        main_layout.addWidget(self.warning_line_widget)

        # Main passphrase display
        passphrase_line = QtWidgets.QHBoxLayout()
        self.passphrase_widget = PassphraseDisplayWidget("")
        passphrase_line.addSpacing(20)
        passphrase_line.addWidget(self.passphrase_widget, 1)

        # Passphrase regeneration button
        passphrase_line.addSpacing(15)
        passphrase_line.addWidget(
            RegenButton([self.gen_passphrase])
        )
        passphrase_line.addSpacing(10)
        main_layout.addStretch()
        main_layout.addLayout(passphrase_line)
        main_layout.addStretch()

        main_layout.addSpacing(15)

        settings_line_box = QtWidgets.QHBoxLayout()
        main_layout.addLayout(settings_line_box)
        settings_line_box.addSpacing(20)

        # Selection box for number of words
        settings_line_box.addWidget(QtWidgets.QLabel(_("Number of words:"), self))
        self.num_words_widget = NumberOfWordsWidget(
                num_words, len(self.wordlist.words), [self.gen_passphrase]
        )
        settings_line_box.addWidget(self.num_words_widget)

        settings_line_box.addStretch()

        file_menu = self.menuBar().addMenu(_("File"))
        self.language_selection_widget = LanguageSelection(
            file_menu,
            self.wordlist.locale,
            self.new_wordlist_locale
        )
        file_menu.addMenu(self.language_selection_widget)
        file_menu.addAction("Open new wordlist").triggered.connect(self.open_new_file)

        # Generate the initial passphrase
        self.gen_passphrase()

    def gen_passphrase(self):
        """
        Generates a passphrase and sets the display widget to show it.
        """
        self.passphrase_widget.setText(
            self.wordlist.gen_passphrase(
                self.num_words_widget.value()
            )
        )

    def new_wordlist_locale(self, locale):
        """
        Opens a new wordlist given a locale.

        Args:
        locale -- New locale to use
        """
        self.wordlist = Wordlist.for_locale(locale)
        self.num_words_widget.set_safe_minimum(len(self.wordlist.words))
        self.gen_passphrase()

    def open_new_file(self):
        """
        Uses the QT file dialog to allow the user to select a the path to a
        new wordlist. It then tries to open the wordlist. If successful,
        sets a new safe minimum number of characters in the passphrase and
        generates a passphrase with the new wordlist.
        """
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')

        if fname[0]:
            if self.open_file(fname[0]):
                self.num_words_widget.set_safe_minimum(len(self.wordlist.words))
                self.gen_passphrase()
                # Clear the checkbox on the language list since we're no longer
                # using that language for the word list.
                self.language_selection_widget.clear_checkmark()

    def open_file(self, path):
        """
        Open a file and use it as the wordlist. Returns True if
        successful, False otherwise.

        Args:
        path -- A string containing path to wordlist.
        """
        try:
            self.wordlist = Wordlist.open_path(path)
        except FileTooLargeExeception:
            ErrorDialog(_(
                "Error: wordlist is too large to open. "
                "Please contact the person or organization you recieved this file from "
                "and inform them of this error."
            )).exec_()
            return False
        except BadWordlistException:
            ErrorDialog(_(
                "Error: wordlist has weird words. "
                "Please contact the person or organization you recieved this file from "
                "and inform them of this error."
            )).exec_()
            return False
        return True


class LanguageSelection(QtWidgets.QMenu):
    """
    Menu item allowing for selection of the language of the wordlist.
    """
    def __init__(self, parent, current_locale, locale_open_func):
        super().__init__(_("Languages"), parent)
        self.setTitle(_("Wordlist language"))

        self.language_group = QtWidgets.QActionGroup(self)

        # map the locale strings to their language (in that language)
        name_locale_mapping = []
        for locale in get_wordlists_by_locale():
            # Ignore locales that aren't territory specific, since these are duplicates
            if locale[1]:
                name_locale_mapping.append((Locale(*locale).display_name, locale))

        # Add the languages to the menu
        for display_name, locale in sorted(name_locale_mapping):
            action = QtWidgets.QAction(display_name, self.language_group)
            action.setCheckable(True)

            # Mark the current selected locale.
            if locale == current_locale:
                action.setChecked(True)

            self.addAction(action)
            action.triggered.connect(functools.partial(locale_open_func, locale))

    def clear_checkmark(self):
        """
        Remove the checkmark next to the currently selected language, if there is one.
        """
        if self.language_group.checkedAction():
            self.language_group.checkedAction().setChecked(False)


class WarningLineWidget(QtWidgets.QLabel):
    """Widget to display warning text"""
    def __init__(self, warning_text):
        super().__init__()
        self.setText(warning_text)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QFont('SansSerif', 14))
        self.setStyleSheet("QLabel { color : red; }")
        self.setWordWrap(True)


class PassphraseDisplayWidget(QtWidgets.QScrollArea):
    """Widget to display the passphrase, with a scollbar when required"""
    def __init__(self, passphrase):
        """
        Args:
        passprase -- a string containing the generated passphrase to display
        """
        super().__init__()
        self.setWidget(self.PassphraseDisplayWidgetText(passphrase))
        self.setWidgetResizable(True)
        self.setStyleSheet(
            """
            QScrollArea {
              border: 1px solid gray;
              border-radius: 2px;
            }
            """
        )

    def setText(self, passphrase):
        """
        Updates the passphrase to display

        Args:
        passphrase -- a string containing the passphrase to display
        """
        self.widget().setText(passphrase)

    class PassphraseDisplayWidgetText(QtWidgets.QLabel):
        """
        Actual class that display the passphrase.
        """
        def __init__(self, passphrase):
            """
            Args:
            passprase -- a string containing the generated passphrase to display
            """
            super().__init__(passphrase)
            self.setFont(QFont('SansSerif', 20))
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setWordWrap(True)
            self.setStyleSheet(
                """
                QLabel {
                  background-color: #ededed;
                  margin-left: 10px;
                  margin-right: 10px;
                }
                """
            )


class RegenButton(QtWidgets.QLabel):
    """A button to regenerate the passphrase"""
    def __init__(self, clicked_fns):
        """
        Args:
        clicked_fn -- An array of functions to be called when the button
                      is clicked.
        """
        super().__init__("")
        for fn in clicked_fns:
            self.clicked.connect(fn)
        self.setPixmap(
            QIcon(os.path.join(os.path.dirname(__file__),
                               "images/sync-alt.svg")).pixmap(25, 25)
        )
        self.setAlignment(QtCore.Qt.AlignCenter)

    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        """Runs when button is clicked."""
        self.clicked.emit()


class NumberOfWordsWidget(QtWidgets.QSpinBox):
    """
    A widget that allows the user to update the number of words to use in
    the passphrase.
    """
    def __init__(self, num_words, wordlist_length, value_changed_fns):
        """
        Args:
        num_words -- number of words to start with. If this is below a safe
                     value it will be raised
        wordlist_length -- number of words in the wordlist
        value_changed_fn -- arrry of functions to call when the user
                            changes the number
        """
        super().__init__()
        self.setValue(num_words)
        self.set_safe_minimum(wordlist_length)

        for fn in value_changed_fns:
            self.valueChanged.connect(fn)

        # Don't allow focus or selection of the value.
        self.setFocusPolicy(0)
        # Style the widget
        self.setFrame(False)
        self.setStyleSheet(
            """
            QSpinBox {
              background-color: #ededed;
              selection-background-color: #ededed;
              selection-color: black;
              font-weight: bold;
              color: black;
            }
            """
        )

    def set_safe_minimum(self, wordlist_length, min_entropy=50):
        """
        Sets a safe minimum number of words based on the length of the wordlist.

        Args:
        wordlist_length -- integer representing the number of words in the wordlist
        min_entropy -- integer representing the minimum acceptable amount of
                       entropy in the passphrase
        """
        self.setRange(math.ceil(min_entropy / math.log2(wordlist_length)), 15)


class ErrorDialog(QtWidgets.QMessageBox):
    """Shows an error dialog"""
    def __init__(self, error_text):
        """
        Args:
        error_text -- the text to show in the dialog box
        """
        super().__init__()
        self.setText(error_text)


app = QtWidgets.QApplication(sys.argv)
