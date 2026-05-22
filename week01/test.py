# tire_volume.py
# CSE 111 - Week 01 Project

# EXCEEDING REQUIREMENTS:
# This version asks the user if they want to get tire newletters.
# If they answer yes, the program stores their email in the volumes.txt file along with the tire information.

import math
from datetime import datetime as dt

width = int(input("Enter the width of the tire in mm (ex 205): "))
aspect_ratio = int(input("Enter the aspect ratio of the tire (ex 60): "))
diameter = int(input("Enter the diameter of the wheel in inches (ex 15): "))

volume = (math.pi * width**2 * aspect_ratio * (width * aspect_ratio + 2540 * diameter) / 10000000000)

print(f"The approximate volume is {volume:.2f} liters")

current_date = dt.now()

newsletter_tires = input("Do you want to subscribe for a newsletter? (yes/no): ").lower()

user_email = ""

# If the user says yes, ask for their email
if newsletter_tires == "yes":
    user_email = input("Please enter your email: ")

with open("volumes.txt", "at") as file:

    if user_email != "":
        print(
            f"{current_date:%Y-%m-%d}, "
            f"{width}, "
            f"{aspect_ratio}, "
            f"{diameter}, "
            f"{volume:.2f}, "
            f"{user_email}",
            file=file
        )

    else:
        print(
            f"{current_date:%Y-%m-%d}, "
            f"{width}, "
            f"{aspect_ratio}, "
            f"{diameter}, "
            f"{volume:.2f}",
            file=file
        )