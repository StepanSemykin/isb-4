import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel,
                             QMainWindow, QMessageBox, QPushButton,
                             QWidget, QAbstractSpinBox, QSpinBox, QProgressBar)
import settings
import stats
import card_number

DEFAULT = 'Files\\settings.json'


class GraphicalInterface(QMainWindow):
    def __init__(self) -> None:
        """Initialization of the application window.
        """
        super(GraphicalInterface, self).__init__()
        self.settings_not_loaded = True
        self.statistic_list = []
        self.setWindowTitle('Card number selection')
        self.setFixedSize(300, 420)
        self.move(800, 200)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.intro = QLabel('You are welcomed by a system that allows you to determine the correct card number by its hash',
                            self.central_widget)
        self.intro.setFont(QFont('Arial', 12))
        self.intro.setGeometry(50, -90, 200, 300)
        self.intro.setWordWrap(True)
        self.intro.setAlignment(Qt.AlignCenter)
        self.settings_file_label = QLabel(
            'SETTINGS FILE:', self.central_widget)
        self.settings_file_label.setGeometry(10, 145, 100, 30)
        self.load_settings_button = QPushButton(
            'LOAD', self.central_widget)
        self.load_settings_button.setToolTip('Сhanges the default settings')
        self.load_settings_button.clicked.connect(self.upload_settings_file)
        self.load_settings_button.setGeometry(190, 145, 100, 30)
        self.cores = QLabel('CORES:', self.central_widget)
        self.cores.setGeometry(10, 200, 100, 30)
        self.cores_spin = QSpinBox(self)
        self.cores_spin.setGeometry(190, 200, 100, 30)
        self.cores_spin.setRange(1, 12)
        self.cores_spin.setStepType(QAbstractSpinBox.DefaultStepType)
        self.card = QLabel('CARD NUMBER: ', self.central_widget)
        self.card.setGeometry(10, 255, 100, 30)
        self.card_button = QPushButton('RECEIVE', self.central_widget)
        self.card_button.setGeometry(190, 255, 100, 30)
        self.card_button.clicked.connect(self.recovery)
        self.stats = QLabel('STATISTICS: ', self.central_widget)
        self.stats.setGeometry(10, 310, 100, 30)
        self.stats_button = QPushButton('SAVE', self.central_widget)
        self.stats_button.setGeometry(190, 310, 100, 30)
        self.stats_button.clicked.connect(self.get_statistic)
        self.hist = QLabel('HISTOGRAM: ', self.central_widget)
        self.hist.setGeometry(10, 365, 100, 30)
        self.hist_button = QPushButton('DRAW', self.central_widget)
        self.hist_button.setGeometry(190, 365, 100, 30)
        self.hist_button.clicked.connect(self.make_historgam)

    def upload_settings_file(self) -> None:
        try:
            self.file_name, _ = QFileDialog.getOpenFileName(
                self, 'Open Settings File', '', 'Settings Files (*.json)')
            self.architecture = settings.Configuration.load_settings(
                self, self.file_name)
            QMessageBox.information(
                self, 'Settings',
                f'Settings successfully loaded from file: {self.file_name}')
        except OSError as err:
            self.file_name = DEFAULT
            self.architecture = settings.Configuration.load_settings(
                self, self.file_name)
            QMessageBox.information(
                self, 'Settings', f'Settings file was not loaded.'
                f' The default settings are set\nPath: {self.file_name}')
        self.settings_not_loaded = False

    def recovery(self) -> None:
        if self.settings_not_loaded:
            QMessageBox.information(self, 'Settings',
                                    f'Settings file was not loaded.'
                                    f' Please download the settings')
            self.upload_settings_file()
        self.pbar = ProgressBar(len(self.architecture['bins']))
        self.pbar.show()
        def increase(count: int) -> None:
            ProgressBar.increase(self.pbar, count)
            QApplication.processEvents()
        start = time.time()
        print(len(self.architecture['bins']))
        self.numbers = card_number.get_number(self.architecture['hash'],
                                              self.architecture['last_numbers'],
                                              self.architecture['bins'],
                                              self.cores_spin.value(),
                                              increase)
        end = time.time()
        self.statistic_list.append([self.cores_spin.value(), end - start])
        self.is_real_numbers = {}
        for i in self.numbers:
            self.correct = card_number.luhn_algorithm(str(i))
            self.is_real_numbers[i] = self.correct
        settings.Configuration.write_card(
            self, self.is_real_numbers, self.file_name)
        QMessageBox.information(self, 'Recovery',
                                f'Card number saved to file: {self.file_name}')

    def get_statistic(self) -> None:
        if self.settings_not_loaded:
            QMessageBox.information(self, 'Settings',
                                    f'Settings file was not loaded.'
                                    f' Please download the settings')
            self.upload_settings_file()
        if not self.statistic_list:
            QMessageBox.information(
                self, 'Statistic', f'There are no statistics.'
                f' Сheck the card numbers')
        else:
            self.data = stats.Stats(self.file_name)
            for i in self.statistic_list:
                self.data.write_stats(i[0], i[1])
            QMessageBox.information(
                self, 'Statistic',
                f' Statistic are loaded from file: {self.data.stats}')

    def make_historgam(self) -> None:
        if self.settings_not_loaded:
            QMessageBox.information(self, 'Settings',
                                    f'Settings file was not loaded.'
                                    f' Please download the settings')
            self.upload_settings_file()
        self.data = stats.Stats(self.file_name)
        self.statistic_dict = stats.Stats.load_stats(self.data)
        self.hist = stats.Stats.draw_histogram(self, self.statistic_dict)
        print(self.statistic_dict)
        stats.Stats.save_histogram(self.data, self.hist)
        QMessageBox.information(
            self, 'Histogram',
            f' Histogram saved from file: {self.data.hist}')


class ProgressBar(QMainWindow):
    def __init__(self, len):
        super().__init__()
        self.setWindowTitle('Progress')
        self.setFixedSize(300, 120)
        self.move(800, 300)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 40, 295, 30)
        self.progress_bar.setMaximum(len)
        self.progress_bar.setValue(0)
        self.per = 0

    def increase(self, count: int) -> None:
        self.progress_bar.setValue(count)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GraphicalInterface()
    w.show()
    sys.exit(app.exec_())
