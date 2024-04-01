from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtCore import QObject, Qt, pyqtSignal, QThread
from config import UI_CONFIG
from widgets import pygame_widget
import driver
import sys, os
sys.path.insert(1, os.getcwd())
import pygame
from rendering import renderer
import time
from utils import logging


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
        #self.pygame.create()

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

        # sim buttons
        self.start_stop_sim_button = QPushButton('Run Simulation', self)
        self.start_stop_sim_button.clicked.connect(self.start_sim_button_click)
        self.start_stop_sim_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')
        self.layout.addWidget(self.start_stop_sim_button, i+2, 1, 1, 1)

        self.pause_unpause_sim_button = QPushButton('Pause Simulation', self)
        self.pause_unpause_sim_button.clicked.connect(self.pause_sim_button_click)
        self.pause_unpause_sim_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')
        self.layout.addWidget(self.pause_unpause_sim_button, i+2, 2,1,1)
        return

    def start_sim_button_click(self):
        print(self.sim_thread.is_running)
        if not(self.sim_thread.is_running):
            self.sim_thread.start()
            self.sim_thread.started_signal.connect(self.sim_started_event)
            self.sim_thread.finished_signal.connect(self.sim_finished_event)
        else:
            self.sim_thread.stop_sim()

    def pause_sim_button_click(self):
        self.sim_thread.pause_unpause_sim()
        if self.sim_thread.pause:
            self.pause_unpause_sim_button.setText("Unpause Simulation")
        else:
            self.pause_unpause_sim_button.setText("Pause Sim")

    def sim_started_event(self, sim_started):
        self.start_stop_sim_button.setText("Stop Simulation")
        self.start_stop_sim_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: red; color: white;')

    def sim_finished_event(self, sim_finished, iteration):
        self.start_stop_sim_button.setText("Start Simulation")
        self.start_stop_sim_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')
        #self.pygame.close()


class SimulationThread(QThread):
    # Define a signal to communicate with the main thread
    started_signal = pyqtSignal(bool)
    finished_signal = pyqtSignal(bool, int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stop = False
        self.pause = False
        self.is_running = False

    def run(self):
        logging.log("INFO", "Starting Simulation", "tab1.SimulationThread", "run")
        sim_driver = driver.SimDriver()
        sim_driver.start_rendering_thread()
        self.iteration = 0
        self.stop = False
        self.pause = False
        self.started_signal.emit(True)
        self.is_running = True
        while(self.stop == False and self.iteration < 5000):
            if(self.pause == False):
                self.iteration = sim_driver.run_iteration(self.iteration)
                time.sleep(.2)
            else:
                time.sleep(1)

        self.is_running = False
        self.stop = False
        self.pause = False

        logging.log("INFO", f"Simulation has finished at iteration: {self.iteration}", "tab1.SimulationThread", "run")
        self.finished_signal.emit(True, self.iteration)
        del(sim_driver)

    def stop_sim(self):
        if(self.is_running):
            logging.log("INFO", f"Stopping Sim at iteration:{self.iteration}", "tab1.SimulationThread", "stop_sim")
            self.stop = True

    def pause_unpause_sim(self):
        if(self.pause == False):
            logging.log("INFO", "Pausing Sim", "tab1.SimulationThread", "pause_unpause_sim")
            self.pause = True
        else:
            logging.log("INFO", "Unpausing Sim", "tab1.SimulationThread", "pause_unpause_sim")
            self.pause = False
