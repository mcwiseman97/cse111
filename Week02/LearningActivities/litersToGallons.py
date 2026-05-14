def lp100k_from_mpg(mpg):
    litersPer100K = 235.215/mpg
    print(f"{litersPer100K:.2f} liters per 100 kilometers")
    return litersPer100K

def miles_per_gallon(start, end, gallons):
    mpg = (end-start)/gallons
    print(f"{mpg:.1f} Miles per Gallon")
    lp100k_from_mpg(mpg)

def main():
    firstReading = float(input("Enter the first odometer reading (miles):"))
    secondReading = float(input("Enter the second odometer reading (miles)"))
    galUsed = float(input("Enter the amount of fuel used (gallons)"))

    miles_per_gallon(firstReading, secondReading, galUsed)

main()



#mpg = end − start/gallons