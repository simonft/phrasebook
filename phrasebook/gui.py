import sys
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QAction, QFileDialog,
                             QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

from phrasebook.passphrase import Wordlist


class PhraseWindow(QMainWindow):
    def __init__(self,
                 word_list_path=None,
                 number_of_words=None,
                 locale=None):
        self.wordlist = Wordlist(path=word_list_path)
        self.initUI(number_of_words=number_of_words)

    def initUI(self, number_of_words=None):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(800, 40))
        self.setWindowTitle("Phrasebook")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout.addSpacing(15)

        # Main passphrase display
        self.passphrase_widget = QLabel(self.wordlist.gen_passphrase(number_of_words), self)
        self.passphrase_widget.setFont(QFont('SansSerif', 20))
        self.passphrase_widget.setAlignment(QtCore.Qt.AlignCenter)
        self.passphrase_widget.setWordWrap(True)
        main_layout.addWidget(self.passphrase_widget)

        main_layout.addSpacing(15)

        settings_line_box = QHBoxLayout()
        main_layout.addLayout(settings_line_box)
        settings_line_box.addSpacing(15)

        # Selection box for number of words
        settings_line_box.addWidget(QLabel("Number of words", self))
        self.num_words_widget = QSpinBox()
        self.num_words_widget.setRange(4, 15)
        self.num_words_widget.setValue(number_of_words)
        self.num_words_widget.valueChanged.connect(self.gen_passphrase)
        settings_line_box.addWidget(self.num_words_widget)

        settings_line_box.addStretch()

        # Passphrase regeneration button
        self.regen_button = QPushButton('New Phrase', self)
        self.regen_button.resize(self.regen_button.minimumSizeHint())
        self.regen_button.clicked.connect(self.gen_passphrase)
        settings_line_box.addWidget(self.regen_button)
        settings_line_box.addSpacing(15)

        main_layout.addSpacing(10)

        # Menu bar
        open_new_wordlist_act = QAction('&Open new wordlist', self)
        open_new_wordlist_act.triggered.connect(self.open_new_file)
        self.statusBar()
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(open_new_wordlist_act)

    def gen_passphrase(self):
        self.passphrase_widget.setText(
            self.wordlist.gen_passphrase(
                self.num_words_widget.value()
            )
        )

    def open_new_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', str(Path.home()))

        if fname[0]:
            self.wordlist = Wordlist(path=fname[0])
            self.gen_passphrase()


app = QtWidgets.QApplication(sys.argv)
