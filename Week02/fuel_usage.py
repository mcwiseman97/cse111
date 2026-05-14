"""
Author: Michael Wiseman
Assignment: miles per gallon & liters per 100 kilomoters
Date: 1/14/26
"""
import math

def main():
  # Get an odometer value in U.S. miles from the user.
  # Get another odometer value in U.S. miles from the user.
  # Get a fuel amount in U.S. gallons from the user.
  # Call the miles_per_gallon function and store
  # the result in a variable named mpg.
  # Call the lp100k_from_mpg function to convert the
  # miles per gallon to liters per 100 kilometers and
  # store the result in a variable named lp100k.
  # Display the results for the user to see.
    
    print()
    start_miles = int(input("Enter the first odometer reading (miles): "))
    end_miles = int(input("Enter the second odometer reading (miles): "))
    print()
    amount_gallons = float(input("Enter the amount of fuel used (gallons): "))

    mpg_efficency = miles_per_gallon(start_miles, end_miles, amount_gallons)
    lp100k_conversion = lp100k_from_mpg(mpg_efficency)
    print()

    print(f"{mpg_efficency:.1f} miles per gallon")

    print(f"{lp100k_conversion:.2f} liters per 100 kilometers")


def miles_per_gallon(start_miles, end_miles, amount_gallons):
    """Compute and return the average number of miles
    that a vehicle traveled per gallon of fuel.
    Parameters
    start_miles: An odometer value in miles.
    end_miles: Another odometer value in miles.
    amount_gallons: A fuel amount in U.S. gallons.
    Return: Fuel efficiency in miles per gallon.
    """
    #miles_driven = end_miles - start_miles
    #efficency = miles_driven / amount_gallons
    efficency = (end_miles - start_miles) / amount_gallons
    return efficency

def lp100k_from_mpg(mpg):
    """Convert miles per gallon to liters per 100
    kilometers and return the converted value.
    Parameter mpg: A value in miles per gallon
    Return: The converted value in liters per 100km.
    """
    lp100k_conversion = 235.215 / mpg
    return lp100k_conversion
# Call the main function so that
# this program will start executing.
main()