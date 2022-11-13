#        _   _ _____              _      _____           _                 
#       | \ | |_   _|            | |    /  ___|         | |                
#       |  \| | | |_ __ __ _  ___| | __ \ `--. _   _ ___| |_ ___ _ __ ___  
#       | . ` | | | '__/ _` |/ __| |/ /  `--. \ | | / __| __/ _ \ '_ ` _ \ 
#       | |\  | | | | | (_| | (__|   <  /\__/ / |_| \__ \ ||  __/ | | | | |
#       \_| \_/ \_/_|  \__,_|\___|_|\_\ \____/ \__, |___/\__\___|_| |_| |_|
#                                               __/ |                      
#                                              |___/                       
#
#
# Author: William Robbers
# Description:
#
# Hello, This is a credit tracking program designed for New Zealand students participating in the NCEA
# (New Zealand Certificate of Educational Achievement).


import sys
import csv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
import PyQt5.QtWidgets

credits_required_by_level = {1: 80, 2: 60, 3: 60}
std_list = []
account = {
    'level': 1,
    'a_credits': 0,
    'm_credits': 0,
    'e_credits': 0
}

HR_to_short = {
    'None': 'None',
    'FUTURE': 'FUTURE',
    'Not Achieved': 'NA',
    'Achieved': 'A',
    'Merit': 'M',
    'Excellence': 'E'
}

short_to_HR = {
    'None': 'None',
    'FUTURE': 'FUTURE',
    'NA': 'Not Achieved',
    'A': 'Achieved',
    'M': 'Merit',
    'E': 'Excellence'
}

priority = {
    'None': 0,
    'FUTURE': 0,
    'NA': 0,
    'A': 1,
    'M': 2,
    'E': 3
}


def window():
    def display_total_credits():
        # Refresh credits
        refresh_credit_totals()

        # Total credits
        level = account['level']
        credits_required = credits_required_by_level[level]
        a_creds = account["a_credits"]
        m_creds = account["m_credits"]
        e_creds = account["e_credits"]
        total_credits = a_creds + m_creds + e_creds
        credits_left = credits_required - total_credits
        credits_left = 0 if credits_left < 0 else credits_left
        percentage = round(total_credits / credits_required * 100, 2)
        percentage = percentage if credits_left > 0 else 100
        total_credits_label.setText(f"Total Credits: {str(total_credits)}/{credits_required}\n{percentage}%")
        ame_credits_label.setText(f"Achieved: {a_creds}\nMerit: {m_creds}\nExcellence: {e_creds}")
        # Endorsement progress
        endorsement_progress_label.setText(f"Merit endorsed: {m_creds + e_creds}/50\nExcellence endorsed: {e_creds}/50")

        # Credits left
        credits_left_label.setText(f"Credits still required: {credits_left}")

        # Pie graph redraw
        series1.clear()
        series1.append("Credits Left", credits_left)
        series1.append("Credits Achieved", total_credits)

        series2.clear()
        series2.append("Achieved", account['a_credits'])
        series2.append("Merit", account['m_credits'])
        series2.append("Excellence", account['e_credits'])

    def refresh_credit_totals():
        account["a_credits"] = 0  #
        account["m_credits"] = 0  # Resit all credits to 0
        account["e_credits"] = 0  #
        for standard in std_list:  # Iterate through student's current enrolled standards
            original_grade = standard[1]
            resit_grade = standard[2]
            if priority[resit_grade] > priority[original_grade]:  # If resit grade is better than original grade
                if priority[resit_grade] != 0:  # If the resit grade is not None or NA
                    key = f"{resit_grade.lower()}_credits"  # Key for account dictionary
                    account[key] += int(standard[3])  # Add the correct grade credits to account
            else:  # If the original grade is better than the resit grade
                if priority[original_grade] != 0:  # If the original grade is not FUTURE or NA
                    key = f"{original_grade.lower()}_credits"  # Key for account dictionary
                    account[key] += int(standard[3])  # Add the correct grade credits to account

    def update_standard():
        std_num = current_standards_table.item(current_standards_table.currentRow(), 0).text()
        entered_original_grade = current_standards_table.cellWidget(current_standards_table.currentRow(), 2).currentText()
        entered_resit_grade = current_standards_table.cellWidget(current_standards_table.currentRow(), 3).currentText()

        if entered_original_grade in ["FUTURE", "Excellence"]:
            entered_resit_grade = "None"

        entered_original_grade = HR_to_short[entered_original_grade]
        entered_resit_grade = HR_to_short[entered_resit_grade]

        for i, std in enumerate(std_list):  # Change original grade
            if std[0] == std_num:
                std[1] = entered_original_grade
                std[2] = entered_resit_grade

        commit_stds_to_file()
        populate_view_standards_table()

    def populate_view_standards_table():
        current_standards_table.clearContents()
        current_standards_table.setRowCount(0)
        row = 0
        for standard in std_list:
            current_standards_table.setRowCount(current_standards_table.rowCount() + 1)  # Add new row to list

            standard_number = QTableWidgetItem(standard[0])
            standard_number.setTextAlignment(Qt.AlignCenter)
            standard_number.setFlags(standard_number.flags() & ~Qt.ItemIsEditable)

            original_grade = QComboBox()
            original_grade.addItem("FUTURE")
            original_grade.addItem("Not Achieved")
            original_grade.addItem("Achieved")
            original_grade.addItem("Merit")
            original_grade.addItem("Excellence")
            original_grade.setCurrentText(short_to_HR[standard[1]])

            resit_grade = QComboBox()
            resit_grade.addItem("None")
            resit_grade.addItem("Not Achieved")
            resit_grade.addItem("Achieved")
            resit_grade.addItem("Merit")
            resit_grade.addItem("Excellence")
            resit_grade.setCurrentText(short_to_HR[standard[2]])
            if original_grade.currentText() in ["FUTURE", "Excellence"]:
                resit_grade.setCurrentIndex(0)
                resit_grade.setEnabled(False)
            else:
                resit_grade.setEnabled(True)
            original_grade.currentIndexChanged.connect(update_standard)
            resit_grade.currentIndexChanged.connect(update_standard)

            credits = QTableWidgetItem(standard[3])
            credits.setTextAlignment(Qt.AlignCenter)
            credits.setFlags(credits.flags() & ~Qt.ItemIsEditable)

            standard_name = QTableWidgetItem(get_std_info(standard[0])[0])
            standard_name.setToolTip(get_std_info(standard[0])[0])
            standard_name.setFlags(standard_name.flags() & ~Qt.ItemIsEditable)

            remove_standard_button = QPushButton("X")
            remove_standard_button.setStyleSheet("QPushButton{background-color: #F54957} QPushButton::hover{background-color: #F42A3B}")
            remove_standard_button.clicked.connect(lambda: remove_standard(current_standards_table.item(current_standards_table.currentRow(), 0).text()))

            current_standards_table.setItem(row, 0, standard_number)
            current_standards_table.setItem(row, 1, standard_name)
            current_standards_table.setCellWidget(row, 2, original_grade)
            current_standards_table.setCellWidget(row, 3, resit_grade)
            current_standards_table.setItem(row, 4, credits)
            current_standards_table.setCellWidget(row, 5, remove_standard_button)

            current_standards_table.verticalHeader().hide()
            row += 1

    def commit_stds_to_file():
        with open("student_standards.txt", 'w') as f:
            f.write(f"level,{account['level']}\n")
            for standard in std_list:
                standard = ",".join(standard) + "\n"
                f.write(standard)

    def remove_standard(std_num):
        for i, std in enumerate(std_list):
            if std[0] == std_num:
                current_standards_table.removeRow(i)
                del std_list[i]

        commit_stds_to_file()

    def update_preview():
        preview = get_std_info(std_num_entry_box.text().strip(" AUS"))
        if preview:
            standard_preview_box.setPlaceholderText(preview[0])
            standard_preview_box.setToolTip(preview[0])
        else:
            standard_preview_box.setPlaceholderText("Invalid standard")
            standard_preview_box.setToolTip("Standard preview window")
        original_grade_entry.setCurrentIndex(0)
        resit_grade_entry.setCurrentIndex(0)

        if preview:
            if preview[2] == "Unit":
                original_grade_entry.model().item(3).setEnabled(False)
                original_grade_entry.model().item(4).setEnabled(False)
                resit_grade_entry.setEnabled(False)

            elif preview[2] == "Achievement":
                original_grade_entry.model().item(3).setEnabled(True)
                original_grade_entry.model().item(4).setEnabled(True)
                resit_grade_entry.setEnabled(True)

    def get_std_info(std):
        with open("master-list.csv", "r") as f:
            for line in csv.reader(f):
                if line[1] == std:
                    return line
            # If standard is not found
            return False

    def error_box(msg):
        err_box = QMessageBox()
        err_box.setText(msg)
        err_box.setWindowTitle("ERROR")
        err_box.setStandardButtons(QMessageBox.Ok)
        err_box.exec_()

    def og_grade_changed():
        std = get_std_info(std_num_entry_box.text().strip(" AUS"))
        if std:
            if std[2] == "Unit":
                original_grade_entry.model().item(3).setEnabled(False)
                original_grade_entry.model().item(4).setEnabled(False)
                resit_grade_entry.setEnabled(False)
            elif std[2] == "Achievement":
                original_grade_entry.model().item(3).setEnabled(True)
                original_grade_entry.model().item(4).setEnabled(True)
                resit_grade_entry.setEnabled(True)

                if original_grade_entry.currentIndex() in [0, 4]:  # Future or Excellence
                    resit_grade_entry.setEnabled(False)
                    resit_grade_entry.setCurrentIndex(0)
                else:
                    resit_grade_entry.setEnabled(True)
                    resit_grade_entry.setCurrentIndex(0)

    def add_standard(entered_std_num, entered_original_grade, entered_resit_grade):
        entered_original_grade = HR_to_short[entered_original_grade]
        entered_resit_grade = HR_to_short[entered_resit_grade]

        # If isn't added, add, else error
        entered_standards = [std[0] for std in std_list]
        if get_std_info(entered_std_num):
            if entered_std_num not in entered_standards:
                std_credits = get_std_info(entered_std_num)[5]
                std_list.append([entered_std_num, entered_original_grade, entered_resit_grade, std_credits])
            else:
                error_box("Error: Standard already entered!")
        else:
            error_box("Standard does not exist or is not Registered/Current!")

        commit_stds_to_file()

    # Create system application window
    app = QApplication(sys.argv)

    # Layouts
    central_layout = QGridLayout()
    add_std_layout = QGridLayout()
    results_layout = QGridLayout()
    view_std_layout = QGridLayout()

    # Size Policies
    HStretch_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    VStretch_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
    FStretch_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    FFixed_Policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    # Fonts
    arial18 = QFont("Arial", 18)
    arial24 = QFont("Arial", 24)

    # Central widget
    central_widget = QWidget()
    central_widget.setMinimumSize(1200, 600)
    central_widget.setGeometry(0, 0, 1200, 400)
    central_widget.setLayout(central_layout)
    central_widget.setWindowTitle("NTrack")

    # Add standard page
    add_std_page = QWidget()
    add_std_page.setLayout(add_std_layout)

    # Remove standard page
    results_page = QWidget()
    results_page.setLayout(results_layout)

    # View standards page
    view_std_page = QWidget()
    view_std_page.setLayout(view_std_layout)

    # Tab setup
    tab_widget = QTabWidget()
    tab_widget.addTab(view_std_page, "View standards")
    tab_widget.addTab(add_std_page, "Add standard")
    tab_widget.addTab(results_page, "Results")
    central_layout.addWidget(tab_widget)

    # Standard number entry
    std_num_entry_box = QLineEdit()
    std_num_entry_box.setPlaceholderText("Enter standard number (e.g 9884)")
    std_num_entry_box.setFont(arial24)
    add_std_layout.addWidget(std_num_entry_box, 0, 0, 2, 1)
    std_num_entry_box.textChanged.connect(update_preview)

    # Original grade combo box
    original_grade_entry = QComboBox()
    original_grade_entry.addItem("FUTURE")
    original_grade_entry.addItem("Not Achieved")
    original_grade_entry.addItem("Achieved")
    original_grade_entry.addItem("Merit")
    original_grade_entry.addItem("Excellence")
    original_grade_entry.setFont(arial18)
    add_std_layout.addWidget(original_grade_entry, 0, 1)
    original_grade_entry.currentIndexChanged.connect(og_grade_changed)

    # Resit grade combo box
    resit_grade_entry = QComboBox()
    resit_grade_entry.setEnabled(False)
    resit_grade_entry.addItem("None")
    resit_grade_entry.addItem("Not Achieved")
    resit_grade_entry.addItem("Achieved")
    resit_grade_entry.addItem("Merit")
    resit_grade_entry.addItem("Excellence")
    resit_grade_entry.setFont(arial18)
    add_std_layout.addWidget(resit_grade_entry, 1, 1)

    # Line break
    lbreak1 = QFrame()
    lbreak1.setFrameShape(QFrame.HLine)
    add_std_layout.addWidget(lbreak1, 2, 0, 1, 2)

    # Standard Preview Box
    standard_preview_box = QLineEdit()
    standard_preview_box.setEnabled(False)
    standard_preview_box.setFont(arial18)
    standard_preview_box.setPlaceholderText("Standard Preview")
    add_std_layout.addWidget(standard_preview_box, 3, 0, 1, 2)

    # Line Break
    lbreak2 = QFrame()
    lbreak2.setFrameShape(QFrame.HLine)
    add_std_layout.addWidget(lbreak2, 4, 0, 1, 2)

    # Add standard button
    add_std_button = QPushButton()
    add_std_button.setText("Add Standard")
    add_std_button.setFont(arial24)
    add_std_button.setSizePolicy(FStretch_policy)
    add_std_button.setStyleSheet("QPushButton{background-color: #26C485} QPushButton::hover{background-color: #21AB74}")
    add_std_layout.addWidget(add_std_button, 5, 0, 1, 2)

    # When the add standard button is clicked, activate function to append to student_standards.txt
    add_std_button.clicked.connect(lambda: add_standard(std_num_entry_box.text().strip("AUS"),
                                                        original_grade_entry.currentText(),
                                                        resit_grade_entry.currentText()))

    # Level label
    level_label = QLabel("Level:")
    level_label.setFont(arial18)
    level_label.setSizePolicy(FFixed_Policy)
    results_layout.addWidget(level_label, 0, 0, Qt.AlignRight)

    # Student NCEA Level
    level_select = QComboBox()
    level_select.setFont(arial18)
    level_select.addItems(["1", "2", "3"])
    level_select.setCurrentIndex(account['level'] - 1)
    level_select.setSizePolicy(FFixed_Policy)
    results_layout.addWidget(level_select, 0, 1, Qt.AlignLeft)
    level_select.currentIndexChanged.connect(lambda: set_level())

    def set_level():
        account["level"] = int(level_select.currentText())
        display_total_credits()
        commit_stds_to_file()

    # Total credits label
    total_credits_label = QLabel()
    total_credits_label.setFont(arial24)
    total_credits_label.setAlignment(Qt.AlignCenter)
    total_credits_label.setSizePolicy(FStretch_policy)
    results_layout.addWidget(total_credits_label, 1, 0)

    # AME Credits
    ame_credits_label = QLabel()
    ame_credits_label.setFont(arial24)
    ame_credits_label.setAlignment(Qt.AlignCenter)
    ame_credits_label.setSizePolicy(FStretch_policy)
    results_layout.addWidget(ame_credits_label, 1, 1)

    # Endorsement progress
    endorsement_progress_label = QLabel()
    endorsement_progress_label.setFont(arial18)
    endorsement_progress_label.setAlignment(Qt.AlignCenter)
    endorsement_progress_label.setSizePolicy(FStretch_policy)
    results_layout.addWidget(endorsement_progress_label, 2, 1)

    # Credits left
    credits_left_label = QLabel()
    credits_left_label.setFont(arial18)
    credits_left_label.setAlignment(Qt.AlignCenter)
    credits_left_label.setSizePolicy(FStretch_policy)
    results_layout.addWidget(credits_left_label, 2, 0)

    tab_widget.currentChanged.connect(lambda: display_total_credits())

    # Total credits pie chart
    series1 = QPieSeries()
    series1.append("Credits Achieved", 0)
    series1.append("Credits Left", 0)
    series1.setLabelsPosition(PyQt5.QtChart.QPieSlice.LabelInsideHorizontal)
    series1.setLabelsVisible(True)

    chart1 = QChart()
    chart1.legend().hide()
    chart1.addSeries(series1)
    chart1.createDefaultAxes()
    chart1.setAnimationOptions(QChart.SeriesAnimations)
    chart1.setTitle("Total progress")

    chart1.legend().setVisible(True)
    chart1.legend().setAlignment(Qt.AlignBottom)

    chartview1 = QChartView(chart1)

    results_layout.addWidget(chartview1, 3, 0)

    # AME Pie Chart
    series2 = QPieSeries()
    series2.append("Achieved", 0)
    series2.append("Merit", 0)
    series2.append("Excellence", 0)
    series2.setLabelsPosition(PyQt5.QtChart.QPieSlice.LabelInsideHorizontal)
    series2.setLabelsVisible(True)

    chart2 = QChart()
    chart2.legend().hide()
    chart2.addSeries(series2)
    chart2.createDefaultAxes()
    chart2.setAnimationOptions(QChart.SeriesAnimations)
    chart2.setTitle("Credit breakdown")

    chart2.legend().setVisible(True)
    chart2.legend().setAlignment(Qt.AlignBottom)

    chartview2 = QChartView(chart2)

    results_layout.addWidget(chartview2, 3, 1)

    # -------------------------------------------------------------------------------------

    # Table with current standards
    current_standards_table = QTableWidget()
    current_standards_table.setColumnCount(6)
    current_standards_table.setHorizontalHeaderLabels(["Standard number", "Standard name", "Grade", "Resit grade", "Credits", "Remove"])
    current_standards_table.setWordWrap(True)
    current_standards_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
    current_standards_table.horizontalHeader().setStyleSheet("::section{background-color: lightgray;}")
    view_std_layout.addWidget(current_standards_table, 0, 0)
    populate_view_standards_table()
    tab_widget.currentChanged.connect(lambda: populate_view_standards_table() if tab_widget.currentIndex() == 0 else True)

    central_widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    with open("student_standards.txt", 'r') as f:
        for i, line in enumerate(f):
            if i == 0:
                metadata = line.strip("\n").split(",")
                account['level'] = int(metadata[1])
            else:
                standard = line.strip("\n").split(",")
                std_list.append(standard)
    window()

# End
# -----------------------------------------------------------------------
