import sys
import csv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
import PyQt5.QtWidgets

credits_required_by_level = {1: 80, 2: 60, 3: 60}
entered_standards = []  # Saves std_num of saved standards
account = {
    'level': 1,
    'a_credits': 0,
    'm_credits': 0,
    'e_credits': 0
}

grade_pairs = {
    'FUTURE': 'FUTURE',
    'Not Achieved': 'NA',
    'Achieved': 'A',
    'Merit': 'M',
    'Excellence': 'E'
}

grade_pairs_2 = {
    'FUTURE': 'FUTURE',
    'NA': 'Not Achieved',
    'A': 'Achieved',
    'M': 'Merit',
    'E': 'Excellence'
}

priority = {
    'FUTURE': 0,
    'NORESIT': 0,
    'NA': 0,
    'A': 1,
    'M': 2,
    'E': 3
}


def window():
    def display_total_credits():
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
        endorsement_progress_label.setText(f"Merit endorsed: {a_creds + e_creds}/50\nExcellence endorsed: {e_creds}/50")

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
        with open("student_standards.txt", 'r') as f:
            account["a_credits"] = 0
            account["m_credits"] = 0
            account["e_credits"] = 0
            for standard in f:
                original_grade = standard.split(",")[1]
                resit_grade = standard.split(",")[3]
                if priority[resit_grade] > priority[original_grade]:
                    if priority[resit_grade] != 0:
                        key = f"{resit_grade.lower()}_credits"
                        account[key] = int(standard.split(",")[4])
                else:
                    if priority[original_grade] != 0:
                        key = f"{original_grade.lower()}_credits"
                        account[key] += int(standard.split(",")[4])
    
    def update_standard(entered_std_num, entered_original_grade, standard_resit, entered_resit_grade):
        remove_standard()
        add_standard(entered_std_num, entered_original_grade, standard_resit, entered_resit_grade)
        populate_view_standards_table()
        
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
                standard_number.setFlags(standard_number.flags() & ~Qt.ItemIsEditable)
                original_grade = QComboBox()
                original_grade.addItem("FUTURE")
                original_grade.addItem("Not Achieved")
                original_grade.addItem("Achieved")
                original_grade.addItem("Merit")
                original_grade.addItem("Excellence")
                original_grade.setCurrentText(grade_pairs_2[standard[1]])
                original_grade.currentIndexChanged.connect(lambda: update_standard(standard[0], original_grade.currentText(), standard[2], standard[3]))
                resit = QComboBox()
                resit.addItem("TRUE")
                resit.addItem("FALSE")
                resit.setCurrentText(standard[2])
                resit_grade = QTableWidgetItem()
                if standard[3] == "NORESIT":
                    pass
                else:
                    resit_grade = QTableWidgetItem(standard[3])
                    resit_grade.setTextAlignment(Qt.AlignCenter)
                credits = QTableWidgetItem(standard[4])
                credits.setTextAlignment(Qt.AlignCenter)
                credits.setFlags(credits.flags() & ~Qt.ItemIsEditable)

                standard_name = QTableWidgetItem(get_std_info(standard[0])[0])
                standard_name.setToolTip(get_std_info(standard[0])[0])
                standard_name.setFlags(standard_name.flags() & ~Qt.ItemIsEditable)

                remove_standard_button = QPushButton("X")
                remove_standard_button.clicked.connect(remove_standard)

                current_standards_table.setItem(row, 0, standard_number)
                current_standards_table.setItem(row, 1, standard_name)
                current_standards_table.setCellWidget(row, 2, original_grade)
                current_standards_table.setCellWidget(row, 3, resit)
                current_standards_table.setItem(row, 4, resit_grade)
                current_standards_table.setItem(row, 5, credits)
                current_standards_table.setCellWidget(row, 6, remove_standard_button)

                current_standards_table.verticalHeader().hide()
                row += 1

    def remove_standard(std_num):
        #std_num = current_standards_table.item(current_standards_table.currentRow(), 0).text()
        current_standards_table.removeRow(current_standards_table.find)

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

    def update_preview():
        preview = get_std_info(std_num_entry_box.text().strip(" AUS"))
        if preview:
            standard_preview_box.setPlaceholderText(preview[0])
            standard_preview_box.setToolTip(preview[0])
        else:
            standard_preview_box.setPlaceholderText("")
            standard_preview_box.setToolTip("Standard preview window")
        original_grade_entry.setCurrentIndex(0)
        standard_resit_checkbox.setChecked(False)
        resit_grade_entry.setCurrentIndex(0)

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
        if original_grade_entry.currentIndex() == 0:  # Future
            standard_resit_checkbox.setChecked(False)
            standard_resit_checkbox.setEnabled(False)
            resit_grade_entry.setEnabled(False)
            resit_grade_entry.setCurrentIndex(0)
        elif original_grade_entry.currentIndex() == 1:  # NA
            standard_resit_checkbox.setEnabled(True)
            resit_grade_entry.model().item(2).setEnabled(False)
            resit_grade_entry.model().item(3).setEnabled(False)
        elif original_grade_entry.currentIndex() == 2:  # A
            standard_resit_checkbox.setEnabled(True)
            resit_grade_entry.model().item(2).setEnabled(True)
            resit_grade_entry.model().item(3).setEnabled(True)
        elif original_grade_entry.currentIndex() == 3:  # M
            standard_resit_checkbox.setEnabled(True)
            resit_grade_entry.model().item(2).setEnabled(True)
            resit_grade_entry.model().item(3).setEnabled(True)
        elif original_grade_entry.currentIndex() == 4:  # E
            standard_resit_checkbox.setChecked(False)
            standard_resit_checkbox.setEnabled(False)
            resit_grade_entry.setEnabled(False)
            resit_grade_entry.setCurrentIndex(0)

    def add_standard(entered_std_num, entered_original_grade, standard_resit, entered_resit_grade):
        entered_original_grade = grade_pairs[entered_original_grade]
        if standard_resit == "TRUE":
            entered_resit_grade = grade_pairs[entered_resit_grade]
        else:
            entered_resit_grade = "NORESIT"

        # If standard exists
        if get_std_info(entered_std_num):
            if entered_std_num not in entered_standards:
                entered_standards.append(entered_std_num)
                standard_credits = get_std_info(entered_std_num)[5]
                student_standards = open("student_standards.txt", "a")
                student_standards.write(','.join([entered_std_num,  entered_original_grade, standard_resit, entered_resit_grade, standard_credits]) + "\n")
                student_standards.close()
            else:
                error_box("Error: Standard already entered")
        else:
            error_box("Error: Standard does not exist or is not registered!")

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
    std_num_entry_box.setPlaceholderText("Enter standard number (e.g 91004)")
    std_num_entry_box.setFont(arial18)
    add_std_layout.addWidget(std_num_entry_box, 0, 0)
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

    # Resit checkbox
    standard_resit_checkbox = QCheckBox()
    standard_resit_checkbox.setText("Resit")
    standard_resit_checkbox.setFont(arial18)
    standard_resit_checkbox.setEnabled(False)
    add_std_layout.addWidget(standard_resit_checkbox, 1, 0)

    # Resit grade combo box
    resit_grade_entry = QComboBox()
    resit_grade_entry.setEnabled(False)
    resit_grade_entry.addItem("Not Achieved")
    resit_grade_entry.addItem("Achieved")
    resit_grade_entry.addItem("Merit")
    resit_grade_entry.addItem("Excellence")
    resit_grade_entry.setFont(arial18)
    add_std_layout.addWidget(resit_grade_entry, 1, 1)
    resit_grade_entry.model().item(2).setEnabled(False)
    resit_grade_entry.model().item(3).setEnabled(False)
    standard_resit_checkbox.clicked.connect(resit_grade_entry.setEnabled)

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
    add_std_layout.addWidget(add_std_button, 5, 0, 1, 2)

    # When the add standard button is clicked, activate function to append to student_standards.txt
    add_std_button.clicked.connect(lambda: add_standard(std_num_entry_box.text().strip("AUS"),
                                                original_grade_entry.currentText(),
                                                str(standard_resit_checkbox.isChecked()).upper(),
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
    level_select.setSizePolicy(FFixed_Policy)
    results_layout.addWidget(level_select, 0, 1, Qt.AlignLeft)
    level_select.currentIndexChanged.connect(lambda: set_level())

    def set_level():
        account["level"] = int(level_select.currentText())
        display_total_credits()

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
    # Load currently enrolled standards from file
    with open("student_standards.txt", 'r') as f:
        for standard in f:
            entered_standards.append(standard.split(',')[0])
    window()
