import sys
import math

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
import qtawesome as qta

from phrasebook.wordlist import (Wordlist,
                                   FileTooLargeExeception,
                                   BadWordlistException)


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

        try:
            self.wordlist = Wordlist(path=word_list_path)
        except FileTooLargeExeception:
            ErrorDialog(
                "Error: wordlist is too large to open. "
                "Please try again with a different file."
            ).exec_()
            sys.exit(1)
        except BadWordlistException:
            ErrorDialog(
                "Error: wordlist has weird words. "
                "Please try again with a different file."
            ).exec_()
            sys.exit(1)

        self.setMinimumSize(QSize(800, 220))
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
        self.update_num_words(num_words)
        passphrase_line.addWidget(self.passphrase_widget, 1)

        # Passphrase regeneration button
        passphrase_line.addSpacing(10)
        passphrase_line.addWidget(
            RegenButton([self.gen_passphrase, self.check_entropy])
        )
        passphrase_line.addSpacing(10)
        main_layout.addLayout(passphrase_line)

        main_layout.addSpacing(15)

        settings_line_box = QtWidgets.QHBoxLayout()
        main_layout.addLayout(settings_line_box)
        settings_line_box.addSpacing(15)

        # Selection box for number of words
        settings_line_box.addWidget(QtWidgets.QLabel("Number of words", self))
        settings_line_box.addWidget(
            NumberOfWordsWidget(
                self.num_words, [self.update_num_words, self.check_entropy]
            )
        )
        settings_line_box.addStretch()
        settings_line_box.addWidget(OpenNewWordlistButton(self.open_new_file))

    def update_num_words(self, num):
        self.num_words = num
        self.gen_passphrase()

    def gen_passphrase(self):
        self.passphrase_widget.setText(
            self.wordlist.gen_passphrase(
                self.num_words
            )
        )

    def check_entropy(self):
        """
        Ensure the entropy from the number of words in the wordlist and in
        the passphrase is high enough.
        """
        if math.log2(len(self.wordlist.words) ** self.num_words) < 50:
            self.warning_line_widget.setText(
                "Warning: " + str(self.num_words) + " words is too few for the "
                "passphrase to be secure with the wordlist you're using."
                "Try increasing the number of words."
            )
        else:
            self.warning_line_widget.setText("")

    def open_new_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')

        if fname[0]:
            try:
                self.wordlist = Wordlist(path=fname[0])
                self.gen_passphrase()
            except FileTooLargeExeception:
                ErrorDialog(
                    "Error: wordlist is too large to open. "
                    "Please contact the person or organization you recieved this file from "
                    "and inform them of this error."
                ).exec_()
            except BadWordlistException:
                ErrorDialog(
                    "Error: wordlist has weird words. "
                    "Please contact the person or organization you recieved this file from "
                    "and inform them of this error."
                ).exec_()


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
        self.setFrameStyle(0)

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
        self.setPixmap(qta.icon('fa.refresh').pixmap(30, 30))
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
    def __init__(self, num_words, value_changed_fns):
        """
        Args:
        num_words -- number of words to start with.
        value_changed_fn -- arrry of functions to call when the user
                            changes the number
        """
        super().__init__()
        self.setRange(4, 15)
        self.setValue(num_words)

        for fn in value_changed_fns:
            self.valueChanged.connect(fn)

        # Don't allow focus or selection of the value.
        self.setFocusPolicy(0)
        # Style the widget
        self.setFrame(False)
        self.setStyleSheet(
            """
            QSpinBox {
              background-color : #efefef;
              selection-background-color : #efefef;
              selection-color: black;
              font-weight: bold;
              color: black;
            }
            QLineEdit {
              border: 0px solid black;
            }
            """
        )


class OpenNewWordlistButton(QtWidgets.QPushButton):
    """
    A button allowing the user to select a custom wordlist. Opens a file
    selection dialog.
    """
    def __init__(self, fn):
        """
        Args:
        fn -- function to call with the updated path.
        """
        super().__init__("Open new wordlist")
        self.clicked.connect(fn)


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
