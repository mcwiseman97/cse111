import math as m

tireWidth = int(input("Enter the width of the tire in mm (ex 205): "))
aspectRatio = int(input("nter the aspect ratio of the tire (ex 60): "))
tireDiameter = int(input("Enter the diameter of the wheel in inches (ex 15): "))
tireVolume = m.pi * (tireWidth**2) * aspectRatio * (tireWidth * aspectRatio + 2540 * tireDiameter) / 10_000_000_000

print(f"The approximate volume is {tireVolume:.2f} liters")