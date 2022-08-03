import csv
#Author: William Robbers
#Date: 4/08/2022
#Version: 0.2

#add links for the nzqa marking schedule and/or exemplars

#Standard Indecies
#[0] Title
#[1] Number
#[2] Type
#[3] Version
#[4] Level
#[5] Credits
#[6] STD Status
#[7] Ver Status
#[8] Field
#[9] SubField
#[10] Domain

#Standard save info
#[0] Type
#[1] Num
#[2] Grade
#[3] Resit
#[4] Resit Grade
#[5] STD Credits

credits_required_by_level = {1:80, 2:60, 3:60}
entered_standards = [] #Saves std_num of saved standards
temp_line_storage = [] #Used for removing lines from student standards
level = 0

def startup():
    level = int(input("What NCEA level are you? "))

def get_credits(std):
    with open("master-list.csv", "r") as f:
        for line in csv.reader(f):
            if line[1] == std:
                f.close()
                return line[5]

def check_std(std):
    with open("master-list.csv", "r") as f:
        for line in csv.reader(f):
            if std in line[1]:
                f.close()
                return True

def add_standard():
    #Takes all standard (std) information to add to student's standard database
    std_num = input("What is the standard number? ")
    if check_std(std_num) == True:
        if std_num in entered_standards:
            print("This standard is already entered!")
            return False
    else:
        print("This standard does not exist or is not current / registered")
        return False
    
    #Fetch credits of standard
    std_credits = get_credits(std_num)
    
    #Initial grade entry
    std_grade = input("What grade did you recieve (short format): ").lower()
    if std_grade in ["na", "a", "m", "e"]:
        std_grade = std_grade.upper()
    else:
        print("Entry failed!")
        return False

    #Resit Y/N
    std_resit = input("Did you resit (Y/N): ").lower()
    if std_resit in ["yes", "y"]:
        std_resit = "TRUE"
    elif std_resit in ["no", "n"]:
        std_resit = "FALSE"
    else:
        print("Entry failed!")
        return False

    #Resit grade entry
    if std_resit == "TRUE":
        std_regrade = input("What was your resit grade? ").lower()
        if std_regrade in ["na", "a", "m", "e"]:
            std_regrade = std_regrade.upper()
        else:
            print("Entry failed!")
            return False
    else:
        std_regrade = "NORESIT"
    
    #Save standard information
    student_standards = open("student_standards.txt", "a")
    student_standards.write(','.join([std_num, std_grade, std_resit, std_regrade, std_credits]) + "\n")
    student_standards.close()

    #Add standard number to list
    entered_standards.append(std_num)

    #Return complete
    return True

def remove_standard(std_num):
    with open("student_standards.txt", "r") as f:
        temp_line_storage = f.readlines()
    with open("student_standards.txt", "w") as f:
        for line in temp_line_storage:
            if std_num not in line:
                f.write(line)
            else:
                print("Removed!")

def show_standards():
    with open("student_standards.txt", "r") as f:
        print("\n")
        for standard in f:
            print(standard.strip("\n"))
        print("\n")

#-----------------------------------------------------------------------------------------------------------------
#Start of main sector

print("Welcome to NTrack System")
print("© William Robbers 2022")

#Load standards into current standards list
with open("student_standards.txt", "r") as f:
    for standard in f:
        entered_standards.append(standard.split(',')[1])

#Main loop
cmd = input("Enter a command: ")
while cmd != "exit":
    if cmd.lower() == "add":
        add_standard()
    
    if cmd.lower() == "remove":
        std_num = input("Enter standard number you would like to remove: ")
        remove_standard(std_num)
    
    if cmd.lower() == "show":
        show_standards()
    
    cmd = input("Enter a command: ")