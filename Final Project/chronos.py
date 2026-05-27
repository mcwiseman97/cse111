import os

FILENAME = 'mind.md'

# Function checks to see if the file exists, create it if its missings
# Returns Boolean value true if and when the file is there
def verify_file(filename):
    print("Checking file status...")
    print(os.listdir())
    if filename in os.listdir():
        print("File exists in directory.")
    else:
        print("file is not in directory, making new file :)")

        with open(FILENAME, 'w') as file:
            file.write("Habits...")
    print("Loading File...")
    return True


def load_file(filename):
    print("File is loading")
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

if __name__ == "__main__":
    main()