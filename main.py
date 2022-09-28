import sys
import csv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

entered_standards = [] #Saves std_num of saved standards

def window():
    def get_std_info(std):
        with open("master-list.csv", "r") as f:
            for line in csv.reader(f):
                if line[1] == std:
                    return line
            #If standard is not found
            return False

    def error_box(msg):
        err_box = QMessageBox()
        err_box.setText(msg)
        err_box.setWindowTitle("ERROR")
        err_box.setStandardButtons(QMessageBox.Ok)
        err_box.exec_()

    def na_selected():
        #Set resit grade to NA everytime original grade is changed
        resit_grade_entry.setCurrentIndex(0)

        #If original grade is not achieved, disable resit for merit or excellence
        if original_grade_entry.currentIndex() == 0:
            resit_grade_entry.model().item(2).setEnabled(False)
            resit_grade_entry.model().item(3).setEnabled(False)
        else:
            resit_grade_entry.model().item(2).setEnabled(True)
            resit_grade_entry.model().item(3).setEnabled(True)
        
        #If original grade is excellence, disable resit checkbox and set resit grade to NA and disable
        if original_grade_entry.currentIndex() == 3:
            standard_resit_checkbox.setChecked(False)
            standard_resit_checkbox.setEnabled(False)
            resit_grade_entry.setEnabled(False)
            resit_grade_entry.setCurrentIndex(0)
        else:
            standard_resit_checkbox.setEnabled(True)
    
    def add_standard():
        entered_std_num = std_num_entry_box.text().strip(" AUS")
        entered_original_grade = original_grade_entry.currentText()
        standard_resit = str(standard_resit_checkbox.isChecked()).upper()
        entered_resit_grade = resit_grade_entry.currentText()

        if entered_std_num == "":
            error_box("Error: Please enter valid standard number!")
            return

        if entered_original_grade == "Not Achieved":
            entered_original_grade = "NA"
        elif entered_original_grade == "Achieved":
            entered_original_grade = "A"
        elif entered_original_grade == "Merit":
            entered_original_grade = "M"
        elif entered_original_grade == "Excellence":
            entered_original_grade = "E"

        if standard_resit == "FALSE":
            entered_resit_grade = "NORESIT"
        
        if entered_resit_grade == "Not Achieved":
            entered_resit_grade = "NA"
        elif entered_resit_grade == "Achieved":
            entered_resit_grade = "A"
        elif entered_resit_grade == "Merit":
            entered_resit_grade = "M"
        elif entered_resit_grade == "Excellence":
            entered_resit_grade = "E"
        
        #If standard exists
        if get_std_info(entered_std_num) != False:
            standard_credits = get_std_info(entered_std_num)[5]
            student_standards = open("student_standards.txt", "a")
            student_standards.write(','.join([entered_std_num, entered_original_grade, standard_resit, entered_resit_grade, standard_credits]) + "\n")
            student_standards.close()
        else:
            error_box("Error: Standard does not exist or is not registered!")
                
    #Create system application window
    app = QApplication(sys.argv)

    #Layouts
    central_layout = QGridLayout()
    add_std_layout = QGridLayout()

    #Size Policies
    HStretch_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    VStretch_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
    FStretch_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    #Fonts
    arial18 = QFont("Arial", 18)
    arial24 = QFont("Arial", 24)

    #Central widget
    central_widget = QWidget()
    central_widget.setMinimumSize(1200,400)
    central_widget.setGeometry(0,0, 1200,400)
    central_widget.setLayout(central_layout)
    
    #Add standard page
    add_std_page = QWidget()
    add_std_page.setLayout(add_std_layout)

    #Tab setup
    tab_widget = QTabWidget(central_widget)
    tab_widget.addTab(add_std_page, "Add standard")
    central_layout.addWidget(tab_widget)

    #Standard number entry
    std_num_entry_box = QLineEdit(tab_widget)
    std_num_entry_box.setPlaceholderText("Enter standard number (e.g 91004)")
    std_num_entry_box.setFont(arial18)
    add_std_layout.addWidget(std_num_entry_box, 0, 0)

    #Original grade combo box
    original_grade_entry = QComboBox(tab_widget)
    original_grade_entry.addItem("Not Achieved")
    original_grade_entry.addItem("Achieved")
    original_grade_entry.addItem("Merit")
    original_grade_entry.addItem("Excellence")
    original_grade_entry.setFont(arial18)
    add_std_layout.addWidget(original_grade_entry, 0, 1)
    original_grade_entry.currentIndexChanged.connect(na_selected)

    #Resit checkbox
    standard_resit_checkbox = QCheckBox(tab_widget)
    standard_resit_checkbox.setText("Resit")
    standard_resit_checkbox.setFont(arial18)
    add_std_layout.addWidget(standard_resit_checkbox, 1, 0)
    standard_resit_checkbox.stateChanged.connect(na_selected)

    #Resit grade combo box
    resit_grade_entry = QComboBox()
    resit_grade_entry.setEnabled(False)
    resit_grade_entry.addItem("Not Achieved")
    resit_grade_entry.addItem("Achieved")
    resit_grade_entry.addItem("Merit")
    resit_grade_entry.addItem("Excellence")
    resit_grade_entry.setFont(arial18)
    add_std_layout.addWidget(resit_grade_entry, 1, 1)
    standard_resit_checkbox.clicked.connect(resit_grade_entry.setEnabled)
    resit_grade_entry.model().item(2).setEnabled(False)
    resit_grade_entry.model().item(3).setEnabled(False)

    #Add standard button
    add_std_button = QPushButton(tab_widget)
    add_std_button.setText("Add Standard")
    add_std_button.setFont(arial24)
    add_std_button.setSizePolicy(FStretch_policy)
    add_std_layout.addWidget(add_std_button, 2, 0, 1, 2)

    #testing
    add_std_button.clicked.connect(add_standard)


    central_widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()