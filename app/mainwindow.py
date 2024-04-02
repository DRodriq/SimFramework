import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit,QPushButton, QMenuBar, QAction
from PyQt5.QtCore import Qt
import os
sys.path.insert(1, os.getcwd())
from config import UI_CONFIG
import datetime
from widgets import tab1, tab2, s_toolbar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.log_buffer = []
        
        self.setGeometry(UI_CONFIG.STRT, UI_CONFIG.END, UI_CONFIG.LEN, UI_CONFIG.WID)
        self.setWindowTitle(UI_CONFIG.WINDOW_TITLE)
        self.session_name = "Session-{}".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.setStyleSheet(f'background-color: {UI_CONFIG.MAIN_THEME}; color: white;')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        toolbar = s_toolbar.Sim_Toolbar()
        self.layout.addWidget(toolbar)

        self.set_title_section()

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f'background-color: {UI_CONFIG.MAIN_THEME}; color: {UI_CONFIG.MAIN_THEME};')
        self.layout.addWidget(self.tab_widget)

        # Create and add tabs
        self.tab_widget.addTab(tab1.Tab1(), UI_CONFIG.TAB_1_TITLE)
        self.tab_widget.addTab(tab2.Tab2(), UI_CONFIG.TAB_2_TITLE)
        self.add_tab("Tab 3")

        self.set_logger_section()

    def add_tab(self, name):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        label = QLabel(f"This is {name}")
        layout.addWidget(label)

        self.tab_widget.addTab(tab, name)

    def set_title_section(self):
        title_label = QLabel(UI_CONFIG.APP_TITLE, self)
        title_label.setStyleSheet('font-size: 36px; font-weight: bold; color: white;')
        self.layout.addWidget(title_label)
        return
    
    def set_logger_section(self):
        # Add Logging window
        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)  # Make it read-only
        self.log_window.setStyleSheet('font-size: 16px; background-color: black; color: white;')
        self.layout.addWidget(self.log_window)  # Adjusted row and column span as needed

        # Add Save Logs button
        self.save_logs_button = QPushButton('Save Session Logs', self)
        self.save_logs_button.clicked.connect(self.save_logs)
        self.save_logs_button.setStyleSheet('font-size: 16px; font-weight: bold; background-color: grey; color: white;')
        self.layout.addWidget(self.save_logs_button)
        return
    
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
    window = MainWindow()
    window.show()
    window.log("Session Started: " + window.session_name, "APP")
    sys.exit(app.exec_())