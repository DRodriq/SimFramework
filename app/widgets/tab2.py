from abc import ABC, abstractmethod
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QPushButton, QTextEdit, QProgressBar, QComboBox, QTabWidget, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
import pyqtgraph
from PyQt5.QtCore import Qt
from config import UI_CONFIG


class Tab2(QWidget):
    def __init__(self):
        super().__init__()

        self.title = UI_CONFIG.TAB_2_TITLE
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.set_section_2()

    def set_section_2(self):
        #label = QLabel(UI_CONFIG.TAB_2_TITLE)
        #label.setStyleSheet('font-size: 20px; font-weight: bold; color: white;')
        #self.layout.addWidget(label, 0, 0, 1, 2)

        self.plot = pyqtgraph.PlotWidget()
        self.layout.addWidget(self.plot, 1, 0)
        self.pen = pyqtgraph.mkPen(color=(255, 255, 255), width=3) #size="20pt")
        self.plot_buffer = []
        self.plot.setTitle("Sample Plot", color = "w")
        self.plot.setLabel("left", "Value")
        self.plot.setLabel("bottom", "Iteration")
        self.plot.showGrid(x=True, y=True)
        self.plot.plotItem.setMouseEnabled(x=False)

        self.clear_plot_button = QPushButton('Clear Plot', self)
        self.clear_plot_button.clicked.connect(self.clear_plot_button_click)
        self.clear_plot_button.setStyleSheet('font-size: 16px; font-weight: bold; background-color: grey; color: white;')
        self.layout.addWidget(self.clear_plot_button, 2, 0)

        self.plot2 = pyqtgraph.PlotWidget()
        self.layout.addWidget(self.plot2, 1, 1)
        self.pen = pyqtgraph.mkPen(color=(255, 255, 255), width=3) #size="20pt")
        self.plot_buffer = []
        self.plot2.setTitle("Sample Plot", color = "w")
        self.plot2.setLabel("left", "Value")
        self.plot2.setLabel("bottom", "Iteration")
        self.plot2.showGrid(x=True, y=True)
        self.plot2.plotItem.setMouseEnabled(x=False)

        self.clear_plot_button2 = QPushButton('Clear Plot', self)
        self.clear_plot_button2.clicked.connect(self.clear_plot_button_click2)
        self.clear_plot_button2.setStyleSheet('font-size: 16px; font-weight: bold; background-color: grey; color: white;')
        self.layout.addWidget(self.clear_plot_button2, 2, 1)

        return

    def clear_plot_button_click(self):
        pass

    def clear_plot_button_click2(self):
        pass