import sys
import csv
from typing import Type
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets
from requests import delete

credits_required_by_level = {1:80, 2:60, 3:60}
entered_standards = [] #Saves std_num of saved standards
account = {
    'level' : 1, 
    'a_credits' : 0, 
    'm_credits' : 0,
    'e_credits' : 0
}

def window():
    def display_total_credits():
        refresh_credit_totals()
        total_credits = account["a_credits"] + account["m_credits"] + account["e_credits"]
        total_credits_label.setText(f"Total Credits: {str(total_credits)}/{credits_required_by_level[account['level']]}\n{total_credits/credits_required_by_level[account['level']]*100}%")
        ame_credits_label.setText(f"Achieved: {account['a_credits']}\nMerit: {account['m_credits']}\nExcellence: {account['e_credits']}")

    def refresh_credit_totals():
        with open("student_standards.txt", "r")  as f:
            account["a_credits"] = 0
            account["m_credits"] = 0
            account["e_credits"] = 0
            for standard in f:
                if standard.split(",")[2] == "TRUE":
                    if standard.split(",")[3] == "A":
                        account["a_credits"] += int(standard.split(",")[4])
                    elif standard.split(",")[3] == "M":
                        account["m_credits"] += int(standard.split(",")[4])
                    elif standard.split(",")[3] == "E":
                        account["e_credits"] += int(standard.split(",")[4])
                else:
                    if standard.split(",")[1] == "A":
                        account["a_credits"] += int(standard.split(",")[4])
                    elif standard.split(",")[1] == "M":
                        account["m_credits"] += int(standard.split(",")[4])
                    elif standard.split(",")[1] == "E":
                        account["e_credits"] += int(standard.split(",")[4])

    def populate_view_standards_table():
        current_standards_table.clearContents()
        current_standards_table.setRowCount(0)
        row = 0
        with open("student_standards.txt", 'r') as student_standards:
            for standard in student_standards:
                standard = standard.strip('\n').split(",")
                current_standards_table.setRowCount(current_standards_table.rowCount() + 1)
                
                standard_number = QTableWidgetItem(standard[0])
                standard_number.setTextAlignment(Qt.AlignCenter)
                original_grade = QTableWidgetItem(standard[1])
                original_grade.setTextAlignment(Qt.AlignCenter)
                resit = QTableWidgetItem(standard[2])
                resit.setTextAlignment(Qt.AlignCenter)
                resit_grade = QTableWidgetItem(standard[3])
                resit_grade.setTextAlignment(Qt.AlignCenter)
                credits = QTableWidgetItem(standard[4])
                credits.setTextAlignment(Qt.AlignCenter)

                standard_name = QTableWidgetItem(get_std_info(standard[0])[0])
                standard_name.setToolTip(get_std_info(standard[0])[0])

                remove_standard_button = QPushButton("X")
                remove_standard_button.clicked.connect(lambda: remove_standard())

                current_standards_table.setItem(row, 0, standard_number)
                current_standards_table.setItem(row, 1, standard_name)
                current_standards_table.setItem(row, 2, original_grade)
                current_standards_table.setItem(row, 3, resit)
                current_standards_table.setItem(row, 4, resit_grade)
                current_standards_table.setItem(row, 5, credits)
                current_standards_table.setCellWidget(row, 6, remove_standard_button)

                current_standards_table.verticalHeader().hide()
                row += 1

    def remove_standard():
        std_num = current_standards_table.item(current_standards_table.currentRow(), 0).text()
        current_standards_table.removeRow(current_standards_table.currentRow())

        with open("student_standards.txt", "r") as f:
            temp_line_storage = f.readlines()
        with open("student_standards.txt", "w") as f:
            for line in temp_line_storage:
                if std_num not in line:
                    f.write(line)
            try:
                entered_standards.remove(std_num)
            except ValueError:
                print("You are not enrolled in this standard!")
                return False

    def show_standard_preview():
        preview = get_std_info(std_num_entry_box.text().strip(" AUS"))
        if preview != False:
            standard_preview_box.setPlaceholderText(preview[0])
            standard_preview_box.setToolTip(preview[0])
        else:
            standard_preview_box.setPlaceholderText("")
            standard_preview_box.setToolTip("Standard preview window")

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

    def reload_all_entries():
        std = get_std_info(std_num_entry_box.text().strip(" AUS"))
        if std != False:
            if std[2] == "Unit":
                original_grade_entry.model().item(2).setEnabled(False)
                original_grade_entry.model().item(3).setEnabled(False)
                standard_resit_checkbox.setEnabled(False)
            elif std[2] == "Achievement":
                #NA Check
                standard_resit_checkbox.setEnabled(True)
                if original_grade_entry.currentIndex() == 0:
                    resit_grade_entry.model().item(2).setEnabled(False)
                    resit_grade_entry.model().item(3).setEnabled(False)
                else:
                    resit_grade_entry.model().item(2).setEnabled(True)
                    resit_grade_entry.model().item(3).setEnabled(True)
                
                #E Check
                if original_grade_entry.currentIndex() == 3:
                    standard_resit_checkbox.setChecked(False)
                    standard_resit_checkbox.setEnabled(False)
                    resit_grade_entry.setEnabled(False)
                    resit_grade_entry.setCurrentIndex(0)
                else:
                    standard_resit_checkbox.setEnabled(True)
        else:
            original_grade_entry.model().item(2).setEnabled(True)
            original_grade_entry.model().item(3).setEnabled(True)
            standard_resit_checkbox.setEnabled(True)
        
        show_standard_preview()
        resit_grade_entry.setCurrentIndex(0)
        
        
        #If original grade is excellence, disable resit checkbox and set resit grade to NA and disable
        
    
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
            if entered_std_num not in entered_standards:
                entered_standards.append(entered_std_num)
                standard_credits = get_std_info(entered_std_num)[5]
                student_standards = open("student_standards.txt", "a")
                student_standards.write(','.join([entered_std_num, entered_original_grade, standard_resit, entered_resit_grade, standard_credits]) + "\n")
                student_standards.close()
            else:
                error_box("Error: Standard already entered")
        else:
            error_box("Error: Standard does not exist or is not registered!")
                
    #Create system application window
    app = QApplication(sys.argv)

    #Layouts
    central_layout = QGridLayout()
    add_std_layout = QGridLayout()
    results_layout = QGridLayout()
    view_std_layout = QGridLayout()

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
    central_widget.setWindowTitle("NTrack")
    
    #Add standard page
    add_std_page = QWidget()
    add_std_page.setLayout(add_std_layout)

    #Remove standard page
    results_page = QWidget()
    results_page.setLayout(results_layout)

    #View standards page
    view_std_page = QWidget()
    view_std_page.setLayout(view_std_layout)

    #Tab setup
    tab_widget = QTabWidget()
    tab_widget.addTab(view_std_page, "View standards")
    tab_widget.addTab(add_std_page, "Add standard")
    tab_widget.addTab(results_page, "Results")
    central_layout.addWidget(tab_widget)

    #Standard number entry
    std_num_entry_box = QLineEdit()
    std_num_entry_box.setPlaceholderText("Enter standard number (e.g 91004)")
    std_num_entry_box.setFont(arial18)
    add_std_layout.addWidget(std_num_entry_box, 0, 0)

    #Original grade combo box
    original_grade_entry = QComboBox()
    original_grade_entry.addItem("Not Achieved")
    original_grade_entry.addItem("Achieved")
    original_grade_entry.addItem("Merit")
    original_grade_entry.addItem("Excellence")
    original_grade_entry.setFont(arial18)
    add_std_layout.addWidget(original_grade_entry, 0, 1)
    original_grade_entry.currentIndexChanged.connect(reload_all_entries)

    #Resit checkbox
    standard_resit_checkbox = QCheckBox()
    standard_resit_checkbox.setText("Resit")
    standard_resit_checkbox.setFont(arial18)
    add_std_layout.addWidget(standard_resit_checkbox, 1, 0)
    standard_resit_checkbox.stateChanged.connect(reload_all_entries)

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

    #Line break
    lbreak1 = QFrame()
    lbreak1.setFrameShape(QFrame.HLine)
    add_std_layout.addWidget(lbreak1, 2, 0, 1, 2)

    #Standard Preview Box
    standard_preview_box = QLineEdit()
    standard_preview_box.setEnabled(False)
    standard_preview_box.setFont(arial18)
    standard_preview_box.setPlaceholderText("hello sir")
    std_num_entry_box.textChanged.connect(lambda: reload_all_entries())
    add_std_layout.addWidget(standard_preview_box, 3, 0, 1, 2)

    #Line Break
    lbreak2 = QFrame()
    lbreak2.setFrameShape(QFrame.HLine)
    add_std_layout.addWidget(lbreak2, 4, 0, 1, 2)

    #Add standard button
    add_std_button = QPushButton()
    add_std_button.setText("Add Standard")
    add_std_button.setFont(arial24)
    add_std_button.setSizePolicy(FStretch_policy)
    add_std_layout.addWidget(add_std_button, 5, 0, 1, 2)

    #When the add standard button is clicked, activate function to append to student_standards.txt
    add_std_button.clicked.connect(add_standard)

    #Student NCEA Level
    level_select = QComboBox()
    level_select.setFont(arial18)
    level_select.addItems(["1", "2", "3"])
    results_layout.addWidget(level_select, 0, 0, 1, 2)
    level_select.currentIndexChanged.connect(lambda: set_level())
    def set_level():
        account["level"] = int(level_select.currentText())
        display_total_credits()


    #Total credits label
    total_credits_label = QLabel()
    total_credits_label.setFont(arial24)
    total_credits_label.setAlignment(Qt.AlignCenter)
    total_credits_label.setSizePolicy(FStretch_policy)
    results_layout.addWidget(total_credits_label, 1, 0)

    #AME Credits
    ame_credits_label = QLabel()
    ame_credits_label.setFont(arial18)
    ame_credits_label.setAlignment(Qt.AlignCenter)
    ame_credits_label.setSizePolicy(FStretch_policy)
    results_layout.addWidget(ame_credits_label, 1, 1)

    tab_widget.currentChanged.connect(lambda: display_total_credits())


    #-------------------------------------------------------------------------------------


    #Table with current standards
    current_standards_table = QTableWidget()
    current_standards_table.setEditTriggers(PyQt5.QtWidgets.QAbstractItemView.NoEditTriggers)
    current_standards_table.setColumnCount(7)
    current_standards_table.setHorizontalHeaderLabels(["Standard number", "Standard name", "Grade", "Resit", "Resit grade", "Credits", "Remove"])
    current_standards_table.setWordWrap(True)
    current_standards_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
    current_standards_table.horizontalHeader().setStyleSheet("::section{background-color: lightgray;}")
    view_std_layout.addWidget(current_standards_table, 0, 0)
    populate_view_standards_table()
    tab_widget.currentChanged.connect(lambda: populate_view_standards_table() if tab_widget.currentIndex() == 0 else True)

    central_widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    #Load currently enrolled standards from file
    with open("student_standards.txt", 'r') as f:
        for standard in f:
            entered_standards.append(standard.split(',')[0])
    window()