"""
Author: Michael Wiseman
Assiignment: Can sizes
Date: 1/14/26
"""
# Volume = math.pi * radius ** 2 * height
# Surface area = 2 * math.pi * (radius + height)
# storage_efficency = volume / surface_area
import math

def main():

    print()
    # Decided to make name / radius / height / cost lists so I can run then through a while loop
    name = ["#1 Picnic", "#1 Tall", "#2", "#2.5", "#3 Cylinder", "#5", "#6Z", "#8Z short", "#10", "#211", "#300", "#303"]
    radius = [6.83, 7.78, 8.73, 10.32, 10.79, 13.02, 5.40, 6.83, 15.72, 6.83, 7.62, 8.10]
    height = [10.16, 11.91, 11.59, 11.91, 17.78, 14.29, 8.89, 7.62, 17.78, 12.38, 11.27, 11.11]
    cost = [0.28, 0.43, 0.45, 0.61, 0.86, 0.83, 0.22, 0.26, 1.53, 0.34, 0.38, 0.42]

    print()

    can_efficency(name, radius, height, cost)


def find_volume(radius, height):
    volume = math.pi * radius ** 2 * height
    return volume

def surf_area(radius, height):
    surface_area = 2 * math.pi * radius * (radius + height)
    return surface_area

def can_efficency(name,radius, height, cost):
    i = 0 # Using i to iterate in the loop from 0 - 12 (there are 12 items in each list [0-11])

    # Add column names for clarity
    print("Can Name\tEfficency \tCost")
    while i < 12:
        volume = find_volume(radius[i], height[i])
        surface_area = surf_area(radius[i], height[i])
        storage_efficency = volume / surface_area

        # Added formatting to clean up the results. Not all results allowed for 2 tabs because of name length.
        if len(name[i]) > 4:
            print(f"{name[i]} \t{storage_efficency:.2f} \t\t${cost[i]:.2f}")
        else:
        #print(f"The {name[i]} can, has an efficency of {storage_efficency:.2f} and the cost of ${cost[i]:.2f}")
            print(f"{name[i]} \t\t{storage_efficency:.2f} \t\t${cost[i]:.2f}")

        i += 1


main()
print()