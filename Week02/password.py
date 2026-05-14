"""
1. Create a folder for this week's project, name it whatever you want.
2. Open the folder you just created in VSCode.
3. Create a file named passwords.py.
4. Add the Constants that define the character lists given from Sven to the top of your code.
5. Create a function definition for each of the functions defined by Sven. Since you won't have any code in your functions yet just add the word pass as the body of your function.
6. Download the following files and save them in your project directory:

USE: open(filename, "r",encoding="utf-8")
"""
import os
cwd = os.getcwd()
#Define Global Variables (Like file location)
#WORDFILE = "./Week2/wordlist.txt"
# "~/Documents/School/cse111/Week2/wordlist.txt"
WORDFILE = "/Users/michaelwiseman/Documents/School/cse111/Week02/wordlist.txt"


def word_in_file(WORDFILE, answer):
    #with open(WORDFILE, "r",encoding="utf-8") as file:
        #for line in file:
            #words = line.split()
            #for word in words:
                #if word == answer:
                    #break
                #else:
                    #return False
            #return True
    pass
    
def word_has_character():
    #LOWER=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    #UPPER=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    #DIGITS=["0","1","2","3","4","5","6","7","8","9"]
    #SPECIAL=["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",", ".", "<", ">", "?", "/", "\\","`", "~"]
    pass
def word_complexity():
    pass
def password_strength(answer):
    word_in_file(WORDFILE,answer)
    word_has_character()
    word_complexity()

    print(answer)

def main():
    
    answer = ""
    # Note that I could have used .lower() to make any answer q or Q.
    while answer != "q" or answer != "Q":
        answer = input("Provide your password: (enter Q to Quit) ")
        if answer == "q" or answer == "Q":
            print("User has quit.")
            return
        print("User provided a valid passoword")
        #word_in_file(WORDFILE, answer)
        password_strength(answer)

if __name__ == "__main__":
    main()