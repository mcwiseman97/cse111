import csv
STUDENT_FILE = "CSE111/W05/Codealong/students.csv"
KEY_INDEX = 0
NAME_INDEX = 1


def read_dictionary(filename, key_column_index):
    s_disctionary = {}

    with open(filename, 'rt') as csv_file:
        #add skip line
        csvreader = csv.reader(csv_file, delimiter=",")
        next(csvreader)
        for row in csvreader:
            key_value = row[key_column_index]
            s_disctionary[key_value] = row
    return s_disctionary

def main():
    STUDENT_FILE = "CSE111/W05/Codealong/students.csv"
    KEY_INDEX = 0
    NAME_INDEX = 1
    students = read_dictionary(STUDENT_FILE, KEY_INDEX)
    inumber = input("Please input an I-Number: ")
    inumber = inumber.replace("-", "") # replace lets you change an instance of an input and or replace that with something else

    if not inumber.isdigit():
        print("Invalid I-Number: Has forign characters!")
    elif len(inumber) != 9:
        if len(inumber) > 9:
            print("Invalid I-Number: I-Number is too long!")
        else:
            print("Invalid I-Number: I-Number is too short!")
    else:
        if inumber in students:

            student = students[inumber]
            name = student[NAME_INDEX]
            print(f"The students name is {name}.")
        else:
            print("No such student!")


if __name__ == "__main__":
    main()