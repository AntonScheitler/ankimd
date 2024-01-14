from PyQt5.QtWidgets import *
from pathlib import Path
import sys


class AnkimdDialog(QDialog):
    def __init__(self):
        super(AnkimdDialog, self).__init__()

        self.resize(300, 200)
        self.setWindowTitle("Ankimd")
        self.filepath = ("", "")
        self.filepath_label = QLabel("")

        self.formGroupBox = QGroupBox()


        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.get_filepath)

        self.delimiter_front_box = QLineEdit("!\\")
        self.delimiter_back_box = QLineEdit("!\\\\")

        # calling the method that create the form
        self.createForm()

        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)

        # adding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)

        # creating a vertical layout
        mainLayout = QVBoxLayout()

        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)

        # adding button box to the layout
        mainLayout.addWidget(self.buttonBox)

        # setting lay out
        self.setLayout(mainLayout)


    def get_filepath(self):
        self.filepath = QFileDialog.getOpenFileName(self, 'Select markdown file to upload',
                                directory=str(Path.home()),
                                filter="*.md")
        self.filepath_label.setText(self.filepath[0])


    def getInfo(self):
        # closing the window
        self.accept()

        # printing the form information
        print("Filepath : {0}".format(self.filepath))
        print("front separator : {0}".format(self.delimiter_front_box.text()))
        print("back separator : {0}".format(self.delimiter_back_box.text()))

# create form method
    def createForm(self):

        # creating a form layout
        layout = QFormLayout()

        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("Upload File"), self.browse_button)
        layout.addWidget(self.filepath_label)

        # for degree and adding combo box
        layout.addRow(QLabel("Delimiter Front"), self.delimiter_front_box)

        # for age and adding spin box
        layout.addRow(QLabel("Delimiter Back"), self.delimiter_back_box)

        # setting layout
        self.formGroupBox.setLayout(layout)


# main method
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnkimdDialog()
    window.show()
    app.exec()
