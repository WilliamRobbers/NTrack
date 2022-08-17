import csv
#Author: William Robbers
#Date: 18/08/2022
#Version: 0.4

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
account = {
    'level' : 0, 
    'a_credits' : 0, 
    'm_credits' : 0,
    'e_credits' : 0
}

def get_std_info(std):
    with open("master-list.csv", "r") as f:
        for line in csv.reader(f):
            if line[1] == std:
                return line
        #If standard is not found
        return False

def add_standard(std_num):
    #Takes all standard (std) information to add to student's standard database

    if get_std_info(std_num) != False:
        if std_num in entered_standards:
            print("This standard is already entered!")
            return False
        else:
            std_credits = get_std_info(std_num)[5]
    else:
        print("This standard does not exist or is not current / registered")
        return False
    
    #Initial grade entry
    std_grade = input("What grade did you recieve (short format): ").lower()
    if std_grade in ["na", "a", "m", "e"]:
        std_grade = std_grade.upper()
    else:
        print("Entry failed!")
        return False

    #Resit Y/N
    std_resit = "FALSE" #default setting
    if std_grade != "E":
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
    try:
        entered_standards.remove(std_num)
    except ValueError:
        print("You are not enrolled in this standard!")
        return False

def show_standards():
    with open("student_standards.txt", "r") as f:
        print("\n")
        for standard in f:
            std = standard.strip("\n").split(",")
            print(f"STD Number: {std[0]}, STD Original grade: {std[1]}, STD Resit: {std[2]}, STD Resit grade: {std[3]}, Credits: {std[4]}")
        print("\n")

def update_standard():
    updated_std_num = input("Which standard would you like to update? ")
    if not remove_standard(updated_std_num) == False:
        add_standard(updated_std_num)

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


#-----------------------------------------------------------------------------------------------------------------
#Start of main sector

print("Welcome to NTrack System")
print("© William Robbers 2022")

#Load standards into current standards list
with open("student_standards.txt", "r") as f:
    for standard in f:
        entered_standards.append(standard.split(',')[0])

#Main loop
cmd = input("Enter a command: ")
while cmd != "exit":
    if cmd.lower() == "add":
        std_num = input("Enter standard number: ")
        add_standard(std_num)
    
    if cmd.lower() == "remove":
        std_num = input("Enter standard number you would like to remove: ")
        remove_standard(std_num)
    
    if cmd.lower() == "show":
        show_standards()

    if cmd.lower() == "update":
        update_standard()
    
    if cmd.lower() == "profile":
        level = int(input("Enter NCEA level: "))
        if level in [1, 2, 3]:
            refresh_credit_totals()
            print(f"Achieved: {account['a_credits']}")
            print(f"Merit: {account['m_credits']}")
            print(f"Excellence: {account['e_credits']}")
            total_credits = account['a_credits'] + account['m_credits'] + account['e_credits']
            print(f"Overall progress: {total_credits}/{credits_required_by_level[level]} -- {(total_credits/credits_required_by_level[level])*100}%")

    cmd = input("Enter a command: ")