#Author: William Robbers
#Date: 7/07/2022
#Version: 0.0

#Standard Indecies
#[0] Title
#[1] Number
#[2] Type
#[3] Version
#[4] Level
#[5] Credits
#[6] Std Status
#[7] Ver Status
#[8] Field
#[9] SubField
#[10] Domain

master_list = open("master-list.csv", "r")
student_standards = open("student_standards.txt", "a")

print("Welcome to NTrack System")
cmd = input("Enter a command: ")

if cmd.lower() == "add":
    print("Complete following information to add a standard to your directory:")
    std_num = input("Standard number: ")
    std_grade = input("Marked grade: ").lower()

    if std_grade == "not achieved" or "na":
        std_grade = "NA"
    elif std_grade == "achieved" or "a":
        std_grade = "A"
    elif std_grade == "merit" or "m":
        std_grade = "M"
    elif std_grade == "excellence" or "e":
        std_grade = "E"
    else:
        True
    


    std_resit = input("Resit (True/False): ").lower()
    if std_resit == "true":
        std_regrade = input("Resit grade: ")
        student_standards.write(','.join([std_num, std_grade, std_resit, std_regrade]) + "\n")
    elif std_resit == "false":
        student_standards.write(','.join([std_num, std_grade, std_resit, "NORESIT"]) + "\n")

student_standards.close()