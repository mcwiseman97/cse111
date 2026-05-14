"""
Author: Michael Wiseman
Assignment: Password strength checker
Date: 5/13/26
"""
import string # used string in my enhancement to simplify character lists instead of the ones below
              #LOWER=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
              #UPPER=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
              #DIGITS=["0","1","2","3","4","5","6","7","8","9"]
              #SPECIAL=["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",", ".", "<", ">", "?", "/", "\\","`", "~"]

# Enhancement: password_strength now returns both a strength score and a message
# so that main() can store a full history of tested passwords and display it on quit.

def word_in_file(word, filename, case_sensative=False):
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if case_sensative:
                if line == word:
                    return True
            else:
                if line.lower() == word.lower():
                    return True
    return False

def word_has_character(word, character_list):
    for character in word:
        if character in character_list:
            return True
    return False

def word_complexity(word):
    # string.ascii_uppercase, string.ascii_lowercase, string.digits, and string.punctuation
    # are premade character lists built into Python's string module (IMPORT STRING TO USE)
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

def password_strength(word, min_length=10, strong_length=16):
    word_list_file = "/Users/michaelwiseman/Documents/School/cse111/Week02/wordlist.txt"
    top_password_file = "/Users/michaelwiseman/Documents/School/cse111/Week02/toppasswords.txt"
    if word_in_file(word, word_list_file, False):
        message = "Password is a dictionary word and is not secure."
        print(message)
        return 0, message
    if word_in_file(word, top_password_file, True):
        message = "Password is a commonly used password and is not secure."
        print(message)
        return 0, message
    if len(word) < min_length:
        message = "Password is too short and is not secure."
        print(message)
        return 1, message
    if len(word) >= strong_length:
        message = "Password is long, length trumps complexity this is a good password."
        print(message)
        return 5, message
    complexity = word_complexity(word)
    strength = 1 + complexity
    message = f"Password Complexity score: {complexity}"
    print(message)
    return strength, message

def main():
    password = ""
    history = []
    while password.lower() != "q":
        print()
        print("To stop testing, type: 'q'")
        password = input("Give me the password to try: ")
        if password.lower() == "q":
            print()
            print("--- Password History ---")
            for entry in history:
                print(f"{entry[0]} - Strength {entry[1]}/5 - {entry[2]}")
            print()
            print("Good luck with your password!")
            return
        else:
            strength, message = password_strength(password)
            print(f"Your password strength is {strength}/5")
            history.append((password, strength, message))

if __name__ == "__main__":
    main()


"""
Future me,  This project tought me about differant ways to use nested functions, 
by making a variable the value of a return of a function. It also solidified 
my understanding of naming variable that pass through functions. 

Need to become more familiar with the "with open()", "for x in y" as it pertains 
to loops and comparing input/ variable to a list
"""