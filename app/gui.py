import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QTextEdit, QProgressBar, QComboBox, QTabWidget, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
import pyqtgraph
import datetime
import os
sys.path.insert(1, os.getcwd())
from config import UI_CONFIG
from widgets import pygame_widget
from rendering import renderer

class ModelTesterUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(UI_CONFIG.STRT, UI_CONFIG.END, UI_CONFIG.LEN, UI_CONFIG.WID)
        self.setWindowTitle(UI_CONFIG.WINDOW_TITLE)
        self.session_name = "Session-{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

        self.render = renderer.Renderer()

        self.log_buffer = []

        self.initUI()

    def initUI(self):
        layout = QGridLayout(self)
        self.setStyleSheet(f'background-color: {UI_CONFIG.MAIN_THEME}; color: white;')

        self.tabs = QTabWidget(self)
        self.tabs.setStyleSheet(f'background-color: {UI_CONFIG.MAIN_THEME}; color: {UI_CONFIG.MAIN_THEME};')
        tab_1 = QWidget()
        tab_2 = QWidget()
        self.tabs.addTab(tab_1, "Training Tab")
        self.tabs.addTab(tab_2, "Dev Tab")

        self.init_tab1(tab_1)
        self.init_tab2(tab_2)

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.pygame_widget = pygame_widget.PygameWidget(self)
        layout.addWidget(self.pygame_widget)

        self.show()

    """
        Tab Construction
    """
    def init_tab1(self, tab_widget):
        current_row = 0
        layout = QGridLayout(tab_widget)
        current_row, layout = self.set_title_section(layout, current_row)
        current_row, layout = self.set_section_1(layout, current_row)
        current_row, layout = self.set_logger_section(layout, current_row)

        tab_widget.setLayout(layout)

    def init_tab2(self, tab_widget):
        layout = QGridLayout(tab_widget)
        current_row = 0
        current_row, layout = self.set_title_section(layout, current_row)

        self.cost_plot = pyqtgraph.PlotWidget()
        layout.addWidget(self.cost_plot, current_row, 0, 3, 3)
        self.pen = pyqtgraph.mkPen(color=(255, 255, 255), width=3) #size="20pt")
        self.cost_data_buffer = []
        self.cost_plot.setTitle("Cost", color = "w")
        self.cost_plot.setLabel("left", "Cost")
        self.cost_plot.setLabel("bottom", "Training Iteration")
        self.cost_plot.showGrid(x=True, y=True)
        self.cost_plot.plotItem.setMouseEnabled(x=False)

        self.clear_cost_plot_button = QPushButton('Clear Plot', self)
        self.clear_cost_plot_button.clicked.connect(self.clear_cost_plot_button_click)
        self.clear_cost_plot_button.setStyleSheet('font-size: 16px; font-weight: bold; background-color: grey; color: white;')
        layout.addWidget(self.clear_cost_plot_button, current_row+4, 0,1,1) 

        tab_widget.setLayout(layout)

    def update_cost_plot(self, cost):
        self.cost_data_buffer.append(cost)
        self.cost_plot.plot(self.cost_data_buffer, pen=self.pen)

    def clear_cost_plot(self):
        self.cost_plot.clear()

    """
        Section Factory
    """
    def set_title_section(self, layout, current_row):
        title_label = QLabel(UI_CONFIG.APP_TITLE, self)
        title_label.setStyleSheet('font-size: 36px; font-weight: bold; color: white;')
        layout.addWidget(title_label, current_row, 0, 1, 6)
        current_row = current_row + 1
        return(current_row, layout)

    def set_section_1(self, layout, current_row):
        section1_label = QLabel(UI_CONFIG.SECTION_1_TITLE, self)
        section1_label.setStyleSheet('font-size: 20px; font-weight: bold; color: white;')
        layout.addWidget(section1_label, current_row, 0)
        current_row = current_row + 1

        current_row = current_row + 1
        
        default_values = UI_CONFIG.SECTION_1_DEFAULTS
        self.input_fields = [QLineEdit(self) for _ in range(len(UI_CONFIG.SECTION_1_LABELS))]

        # input fields
        for i, (label, input_field) in enumerate(zip(UI_CONFIG.SECTION_1_LABELS, self.input_fields), start=0):
            label_widget = QLabel(label, self)
            label_widget.setStyleSheet('font-size: 20px; color: white;')  # Increase font size for labels
            input_field.setText(str(default_values[i]))
            input_field.setStyleSheet('font-size: 16px; color: white;')
            layout.addWidget(label_widget, current_row, 0, 1, 1)
            layout.addWidget(input_field, current_row, 1, 1, 1)
            current_row = current_row + 1

        # data buttons
        self.start_simulation_button = QPushButton('Start Simulation', self)
        self.start_simulation_button.clicked.connect(self.start_simulation_button_click)
        self.start_simulation_button.setStyleSheet(f'font-size: 16px; font-weight: bold; background-color: {UI_CONFIG.SECONDARY_THEME}; color: white;')
        layout.addWidget(self.start_simulation_button, current_row, 1)

        current_row = current_row + 1

        return(current_row, layout)
    
    
    def set_logger_section(self, layout, current_row):
        # Add Logging window
        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)  # Make it read-only
        self.log_window.setStyleSheet('font-size: 16px; background-color: black; color: white;')
        layout.addWidget(self.log_window, current_row, 0, 1, 2)  # Adjusted row and column span as needed
        current_row = current_row + 1

        # Add Save Logs button
        self.save_logs_button = QPushButton('Save Session Logs', self)
        self.save_logs_button.clicked.connect(self.save_logs)
        self.save_logs_button.setStyleSheet('font-size: 16px; font-weight: bold; background-color: grey; color: white;')
        layout.addWidget(self.save_logs_button, current_row, 0,1,1)
        return(current_row, layout)


    def set_plotter_section(self, layout, current_row, plot_labels):
        return(current_row, layout)

    """
        Button Click
    """  
    def start_simulation_button_click(self):
        self.render.start_rendering()

    def clear_dataset_button_click(self):
        pass
    
    def initialize_model_button_click(self):
        pass

    def validate_train_model_button(self):
        pass
        
    def clear_model_button_click(self):
        pass

    def clear_cost_plot_button_click(self):
        pass

    def save_model_button_click(self):
        pass

    def load_model_button_click(self):
        pass

    def train_model_button_click(self):
        pass

    def test_model_button_click(self):
        pass


    """
        Window and Plot Utils
    """   
    def log(self, message, tag="DEFAULT"):
        # Function to log messages to the QTextEdit
        now = datetime.datetime.now()
        message = "[{}] [{}] ".format(now.strftime("%m/%d/%Y-%H:%M:%S"), tag) + message
        self.log_window.append(message)
        if(message.count("Writing logs to") == 0):
            self.log_buffer.append(message)

    def save_logs(self):
        proj_dir = os.path.dirname(os.path.realpath(__file__))
        results_folder = proj_dir + "\\..\\results\\"
        results_file = results_folder + "logs\\" + self.session_name
        self.log("Writing logs to {}".format(results_file), "SYS")
        f = open(results_file, "a")
        for i in range(len(self.log_buffer)):
            f.write(str(self.log_buffer[i])+"\n")
        self.log_buffer.clear()
        f.close()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModelTesterUI()
    
    window.log("Session Started: " + window.session_name, "APP")
    sys.exit(app.exec_())