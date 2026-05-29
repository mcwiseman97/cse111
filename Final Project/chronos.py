import os

FILENAME = 'mind.md'

# Function checks to see if the file exists, create it if its missings
# Returns Boolean value true if and when the file is there
def verify_file(filename):
    print(os.listdir())
    if filename in os.listdir():
        print("File exists in directory.")
    else:
        print("file is not in directory, making new file :)")
        with open(FILENAME, 'w') as file:
            file.write("Habits...")
    print("File loaded successfully.")
    return True


def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)

def add_habit():
    pass

def remove_habit():
    pass
    
def save_file(filename, lines_list):
    pass

def display_dashboard(metrics_dict):
    pass

def main():

    print("Welcome to Chronos! Lets work on your habits!")
    print(f"Your habits are stored in the {FILENAME} file.")

    verify_file(FILENAME)
    load_file(FILENAME)

    print()
    active = True
    while active:
        print("Main Menu")
        print("1. View habits")
        print("2. Show streaks")
        print("0. Quit program")
        print()
        user_answer = int(input(""))
        if user_answer == 1:
            print("Launch Habit View")
        elif user_answer == 2:
            print("Launch Streak View")
        elif user_answer == 0:
            print("Quitting application")
            active = False
        else:
            print("Invalid option: try again.")
            pass


if __name__ == "__main__":
    main()