#Author: William Robbers
#Date: 28/07/2022
#Version: 0.1

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

#Standard save info
#[0] Type
#[1] Num
#[2] Grade
#[3] Resit
#[4] Resit Grade

master_list = open("master-list.csv", "r")
entered_standards = [] #Saves std_num of saved standards
temp_line_storage = [] #Used for removing lines from student standards

def add_standard():
    #Standard type entry
    std_type = input("What type of standard is it? ").lower()

    if std_type in ["as", "us"]:
        std_type = std_type.upper()
    else:
        print("Entry failed!")
        return False

    #Standard number entry
    std_num = input("What is the standard number? ")

    if std_num in entered_standards:
        print("This standard is already entered!")
        return False

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
    student_standards.write(','.join([std_type, std_num, std_grade, std_resit, std_regrade]) + "\n")
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
    True

#-----------------------------------------------------------------------------------------------------------------
#Start of main sector

print("Welcome to NTrack System")
print("© William Robbers 2022")

#Load standards into list
with open("student_standards.txt", "r") as f:
    for standard in f:
        entered_standards.append(standard.split(',')[1])

#Main loop
cmd = input("Enter a command: ")
while cmd != "exit":
    if cmd.lower() == "add":
        is_complete = add_standard()
        print(f"Completion status: {is_complete}")
    
    if cmd.lower() == "remove":
        std_num = input("Enter standard number you would like to remove: ")
        remove_standard(std_num)
    
    if cmd.lower() == "my_standards":
        True
    
    cmd = input("Enter a command: ")

master_list.close()