import sys
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
import qtawesome as qta

from phrasebook.passphrase import Wordlist


class PhraseWindow(QtWidgets.QMainWindow):
    def __init__(self,
                 word_list_path=None,
                 num_words=None,
                 locale=None):
        QtWidgets.QMainWindow.__init__(self)
        self.wordlist = Wordlist(path=word_list_path)
        self.num_words = num_words
        self.initUI()

    def initUI(self):
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

        # Menu bar
        open_new_wordlist_act = QtWidgets.QAction('&Open new wordlist', self)
        open_new_wordlist_act.triggered.connect(self.open_new_file)
        self.statusBar()
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(open_new_wordlist_act)

    def update_num_words(self, num):
        print(num)
        self.num_words = num
        self.gen_passphrase()

    def gen_passphrase(self):
        self.passphrase_widget.setText(
            self.wordlist.gen_passphrase(
                self.num_words
            )
        )

    def open_new_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', str(Path.home()))

        if fname[0]:
            self.wordlist = Wordlist(path=fname[0])
            self.gen_passphrase()


class PassphraseDisplayWidget(QtWidgets.QLabel):
    def __init__(self, passphrase):
        super().__init__(passphrase)
        self.setFont(QFont('SansSerif', 20))
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setWordWrap(True)


class RegenButton(QtWidgets.QLabel):
    def __init__(self, clicked_fn):
        super().__init__("")
        self.clicked.connect(clicked_fn)
        self.setPixmap(qta.icon('fa.refresh').pixmap(30, 30))
        self.setAlignment(QtCore.Qt.AlignCenter)

    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()


class NumberOfWordsWidget(QtWidgets.QSpinBox):
    def __init__(self, num_words, value_changed_fn):
        super().__init__()
        self.setRange(4, 15)
        self.setValue(num_words)
        self.valueChanged.connect(value_changed_fn)


app = QtWidgets.QApplication(sys.argv)
