#TODO: Get user imput on how many manufactured items are available and how many items are needed to fill a box. Then calculate how many boxes can be filled and how many items are left over.   

manufacturedItems = int(input("How mant itesm do you have? "))
boxCapacity = int(input("How many items fit in a box? "))

neededBoxes = manufacturedItems / boxCapacity

print(f"You will need need {neededBoxes} boxes but will have a some left over.")