import math as m
import datetime from datetime

dt = datetime

tireWidth = int(input("Enter the width of the tire in mm (ex 205): "))
aspectRatio = int(input("nter the aspect ratio of the tire (ex 60): "))
tireDiameter = int(input("Enter the diameter of the wheel in inches (ex 15): "))

tireVolumeL = m.pi * (tireWidth**2) * aspectRatio * (tireWidth * aspectRatio + 2540 * tireDiameter) / 10_000_000_000

print(f"The approximate volume is {tireVolumeL:.2f} liters")






#Get the current date from the computer’s operating system.
#Open a text file named volumes.txt for appending.
#Append to the end of the volumes.txt file one line of text that contains the following five values:
# 1. current date (Do NOT include time)
# 2. width of the tire
# 3. aspect ratio of the tire
# 4. diameter of the wheel
# 5. volume of the tire (rounded to two decimal places)