import math

manufacturedItems = int(input("How mant itesm do you have? "))
boxCapacity = int(input("How many items fit in a box? "))

neededBoxes = math.ceil(manufacturedItems / boxCapacity)

print(f"For {manufacturedItems} items, packing {boxCapacity} items in each box, you will need {neededBoxes} boxes.")

# The math.ceil() function required a call to "import math" for the function to work
# The function tell an equasion or value to round up to the neirest 1. 
# If not included, the program would leave out remainders of a number. 