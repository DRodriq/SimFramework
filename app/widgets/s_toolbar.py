from PyQt5.QtWidgets import QMenuBar, QAction, QWidget


class Sim_Toolbar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_toolbars()

    def create_toolbars(self):
        actionFile = self.addMenu("File")
        new_action = QAction("New", self)
        new_action.triggered.connect(self.on_new)
        actionFile.addAction(new_action)
        actionFile.addAction("Open")
        actionFile.addAction("Save")
        actionFile.addSeparator()
        actionFile.addAction("Quit")
        self.addMenu("Edit")
        self.addMenu("View")
        self.addMenu("Help")

    def on_new(self):
        print("New Action Triggered")

    def on_open(self):
        print("Open Action Triggered")

    def on_save(self):
        print("Save Action Triggered")


    def file_new_button_click(self):
        self.close()