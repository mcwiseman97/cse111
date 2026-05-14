"""
Author: Michael Wiseman
Assignment: Password strength checker
Date: 5/13/26
"""
import string # will be used in my enhancement to the code in lines 30-36 to simplify character lists

def word_in_file(word, filename, case_sensative):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if case_sensative:
                if line == word:
                    return True
                else:
                    if line.lower() == word.lower():
                        return True                  

def word_has_character(word, character_list):  
    for character in word:
        if character in character_list:
            return True
    return False
            
def word_complexity(word):
    # The instructions proviide a list for Lower / Upper / Digits / Special but there is a simplified string constant
    # that is string.ascii_lowercaser string.ascii_uppercase string.digits and special is called string.punctuation.
    # Essentially premade lists (IMPORT STRING TO WORK)
    complexity = 0 
    if word_has_character(word, string.ascii_uppercase):
        complexity += 1
    if word_has_character(word, string.ascii_lowercase):
        complexity += 1
    if word_has_character(word, string.digits):
        complexity += 1
    if word_has_character(word, string.punctuation):
        complexity += 1        
    return complexity

# converted password to just 'word'
def password_strength(word, min_length=10, strong_length=16):
    word_list_file = "/Users/michaelwiseman/Documents/School/cse111/Week02/wordlist.txt"
    top_password_file = "/Users/michaelwiseman/Documents/School/cse111/Week02/wordlist.txt"
    # Both call the same function but pass a differant file name through so that it checks both files in one function
    if word_in_file(word, word_list_file, True):
        print("This password can be found in a disctionary.")
        return 0
    if word_in_file(word, top_password_file, True):
        print("This is a common passwords")
        return 0
    if len(word) < min_length:
        print("The password is too short.")
        return 1
    if len(word) >= strong_length:
        print("This password is very strong.")
        return 5
    complexity = word_complexity(word)
    strength = 1 + complexity
    print(f"Password Complexity score: {complexity}")
    return strength

def main():
    password = ""
    while password.lower() != "q":
        print()
        print("To stop testing, type: 'q'")
        password = input("Give me the password to try: ")
        if password.lower() == "q":
            print("Good luck with your password!")
            return
        else:
            strength = password_strength(password)
            print(f"Your password strength is {strength}/5")

if __name__ == "__main__":
    main()


"""
Future me,  This project tought me about differant ways to use nested functions, 
using making a variable the value of a return of a function. It also solidified 
my understanding of naming variable that pass through functions. 

Need to become more familiar with the "with open()", "for x in y" as it pertains 
to loops and comparing input/ variable to a list
"""