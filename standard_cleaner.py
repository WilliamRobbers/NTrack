import csv

dirty_list = open("list-of-all-standards-2020.csv")
clean_list = open("master-list.csv", "w", newline="")

for line in csv.reader(dirty_list):
    if line[7].lower() == "current" and line[4].lower() in ["1", "2", "3"] and line[6].lower() != "expired":
        csv.writer(clean_list).writerow(line)