# Subtract your age from 220 to get maximum heart rate
# Keep your heart between 85%-65% to strengthen heart

userAge = int(input("Please enter your age: "))

maxHeartRate = 220 - userAge

lowHeartRate = int(maxHeartRate * .65)
highHearRate = int(maxHeartRate * .85)



print(f"When you exercise to strengthen your heart, you should keep your heart rate between {lowHeartRate} and {highHearRate} beats per minute.")