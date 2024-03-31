from abc import ABC, abstractmethod
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QPushButton, QTextEdit, QProgressBar, QComboBox, QTabWidget, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
import pyqtgraph
import datetime
from PyQt5.QtCore import Qt
import os
from config import UI_CONFIG

class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        self.title = UI_CONFIG.SECTION_1_TITLE
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        label = QLabel(f"This is {self.title}")
        self.layout.addWidget(label)
        self.set_section_1()

    def set_section_1(self):
        section1_label = QLabel(UI_CONFIG.SECTION_1_TITLE, self)
        section1_label.setStyleSheet('font-size: 20px; font-weight: bold; color: white;')
        self.layout.addWidget(section1_label)
        
        default_values = UI_CONFIG.SECTION_1_DEFAULTS
        self.input_fields = [QLineEdit(self) for _ in range(len(UI_CONFIG.SECTION_1_LABELS))]

        # input fields
        for i, (label, input_field) in enumerate(zip(UI_CONFIG.SECTION_1_LABELS, self.input_fields), start=0):
            label_widget = QLabel(label, self)
            label_widget.setStyleSheet('font-size: 20px; color: white;')  # Increase font size for labels
            input_field.setText(str(default_values[i]))
            input_field.setStyleSheet('font-size: 16px; color: white;')

            self.layout.addWidget(label_widget)
            self.layout.addWidget(input_field)

        # data buttons
        start_simulation_button = QPushButton('Start Simulation', self)
        start_simulation_button.clicked.connect(self.start_simulation_button_click)
        start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')
        self.layout.addWidget(start_simulation_button)

        return

    def start_simulation_button_click(self):
        pass