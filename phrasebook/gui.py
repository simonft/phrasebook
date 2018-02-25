import sys
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
import qtawesome as qta

from phrasebook.passphrase import Wordlist


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
        self.wordlist = Wordlist(path=word_list_path)
        self.num_words = num_words

        self.setMinimumSize(QSize(800, 220))
        self.setWindowTitle("Phrasebook")

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout.addSpacing(15)

        # Main passphrase display
        passphrase_line = QtWidgets.QHBoxLayout()
        self.passphrase_widget = PassphraseDisplayWidget(
            self.wordlist.gen_passphrase(self.num_words)
        )
        passphrase_line.addWidget(self.passphrase_widget, 1)

        # Passphrase regeneration button
        passphrase_line.addSpacing(10)
        passphrase_line.addWidget(RegenButton(self.gen_passphrase))
        passphrase_line.addSpacing(10)
        main_layout.addLayout(passphrase_line)

        main_layout.addSpacing(15)

        settings_line_box = QtWidgets.QHBoxLayout()
        main_layout.addLayout(settings_line_box)
        settings_line_box.addSpacing(15)

        # Selection box for number of words
        settings_line_box.addWidget(QtWidgets.QLabel("Number of words", self))
        settings_line_box.addWidget(NumberOfWordsWidget(self.num_words,
                                                        self.update_num_words))
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

    def open_new_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')

        if fname[0]:
            self.wordlist = Wordlist(path=fname[0])
            self.gen_passphrase()


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
    def __init__(self, clicked_fn):
        """
        Args:
        clicked_fn -- A function that will regenerate and reset the passphrase.
                      This will be called when the button is clicked.
        """
        super().__init__("")
        self.clicked.connect(clicked_fn)
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
    def __init__(self, num_words, value_changed_fn):
        """
        Args:
        num_words -- number of words to start with.
        value_changed_fn -- function to call when the user changes the number
        """
        super().__init__()
        self.setRange(4, 15)
        self.setValue(num_words)
        self.valueChanged.connect(value_changed_fn)


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


app = QtWidgets.QApplication(sys.argv)
