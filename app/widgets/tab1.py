from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from config import UI_CONFIG
from rendering import renderer
import driver
import sys, os
sys.path.insert(1, os.getcwd())


class Tab1(QWidget):
    def __init__(self):
        super().__init__()

        #self.render = renderer.Renderer()

        self.title = UI_CONFIG.TAB_1_TITLE
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.set_section_1()

    def set_section_1(self):
        #section1_label = QLabel(UI_CONFIG.TAB_1_TITLE, self)
        #section1_label.setStyleSheet('font-size: 20px; font-weight: bold; color: white;')
        #self.layout.addWidget(section1_label, 0, 0, 1, 2)
        
        default_values = UI_CONFIG.TAB_1_DEFAULTS
        self.input_fields = [QLineEdit(self) for _ in range(len(UI_CONFIG.TAB_1_LABELS))]

        # input fields
        for i, (label, input_field) in enumerate(zip(UI_CONFIG.TAB_1_LABELS, self.input_fields), start=0):
            label_widget = QLabel(label, self)
            label_widget.setStyleSheet('font-size: 20px; color: white;')  # Increase font size for labels
            input_field.setText(str(default_values[i]))
            input_field.setStyleSheet('font-size: 16px; color: white;')

            self.layout.addWidget(label_widget, i+1, 0)
            self.layout.addWidget(input_field, i+1, 1)

        # data buttons
        start_simulation_button = QPushButton('Start Simulation', self)
        start_simulation_button.clicked.connect(self.start_simulation_button_click)
        start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')
        self.layout.addWidget(start_simulation_button, i+2, 0, 1, 2)

        start_simulation_button = QPushButton('Start Simulation', self)
        start_simulation_button.clicked.connect(self.start_simulation_button_click)
        start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')
        self.layout.addWidget(start_simulation_button, i+2, 0, 1, 2)

        return

    def start_simulation_button_click(self):
        self.sim_thread = SimulationThread()
       # self.render_thread = RendererThread()  
        #self.thread.update_signal.connect(self.update_ui)
        #self.render_thread.start()
        self.sim_thread.start()



class SimulationThread(QThread):
    # Define a signal to communicate with the main thread
    update_signal = pyqtSignal(int)

    def run(self):
        sim_driver = driver.SimDriver()
        sim_driver.run()


class RendererThread(QThread):

    def run(self):
        render = renderer.Renderer()
        render.start_rendering()