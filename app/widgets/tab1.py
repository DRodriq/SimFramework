from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QThread
from config import UI_CONFIG
from widgets import pygame_widget
import driver
import sys, os
sys.path.insert(1, os.getcwd())
import pygame
from rendering import renderer


class Tab1(QWidget):
    def __init__(self):
        super().__init__()

        self.sim_thread = SimulationThread()

        self.title = UI_CONFIG.TAB_1_TITLE
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.set_section_1()
        self.pygame = pygame_widget.PygameWidget(self)
        self.layout.addChildWidget(self.pygame)

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
        self.start_simulation_button = QPushButton('Start Simulation', self)
        self.start_simulation_button.clicked.connect(self.start_simulation_button_click)
        self.start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')
        self.layout.addWidget(self.start_simulation_button, i+2, 0, 1, 2)

        return

    def start_simulation_button_click(self):
        if not(self.sim_thread.isRunning()):
            self.pygame.create()
            self.sim_thread.start()
            self.sim_thread.finished_signal.connect(self.sim_finished)
            self.start_simulation_button.setText("Stop Simulation")
            self.start_simulation_button.clicked.connect(self.stop_simulation_button_click)
            self.start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: red; color: white;')
            #self.layout.addWidget(self.start_simulation_button, i+2, 0, 1, 2)
        else:
            self.start_simulation_button.clicked.connect(self.stop_simulation_button_click)
            self.start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: red; color: white;')     

    def stop_simulation_button_click(self):
        if self.sim_thread.isRunning():
            print("sim is running - got signal to close")
            self.sim_thread.quit()
            self.pygame.close()
            stop_rendering = pygame.event.Event(renderer.STOP_RENDERING, message=False)
            pygame.event.post(stop_rendering)

        else:
            self.start_simulation_button.setText("Start Simulation")
            self.start_simulation_button.clicked.connect(self.start_simulation_button_click)
            self.start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')

        
    def sim_finished(self):
        stop_rendering = pygame.event.Event(renderer.STOP_RENDERING, message=False)
        pygame.event.post(stop_rendering)
        self.start_simulation_button.setText("Start Simulation")
        self.start_simulation_button.clicked.connect(self.start_simulation_button_click)
        self.start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')


class SimulationThread(QThread):
    # Define a signal to communicate with the main thread
    finished_signal = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        sim_driver = driver.SimDriver()
        fin = sim_driver.run()
        if(fin is not None):
            self.finished_signal.emit(True)
        else:
            self.finished_signal.emit(False)
        self.exit()
