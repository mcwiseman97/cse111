from datetime import datetime

dayOfWeek = 0
discount = 1
salesTax = .06
# dayOfWeekNum = datetime.today().weekday()
dayOfWeekNum = 2

weekDay = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(f"The day is {weekDay[dayOfWeekNum]}.")


subtotal = float(input("What was your subtotal: "))

if dayOfWeekNum == 1 or dayOfWeekNum == 2:
    if subtotal >= 50:
        discount = .1
    else:
        discount = 1

totalTax = (subtotal - (subtotal * discount)) * salesTax
total = (subtotal - (subtotal * discount)) + totalTax
print(f"Total: {total:.2f}")

#Not complete. Breaks


# subtotal = 50


# FOR A VERY LONG VERSION - USE THIS METHOD 😂
#if dayOfWeekNum == 0:
#    dayOfWeek = "Monday"
#elif dayOfWeekNum == 1:
#    dayOfWeek = "Tuesday"
#elif dayOfWeekNum == 2:
#    dayOfWeek = "Wednesday"
#elif dayOfWeekNum == 3:
#    dayOfWeek = "Thursday"
#elif dayOfWeekNum == 4:
#    dayOfWeek = "Friday"
#elif dayOfWeekNum == 5:
#    dayOfWeek = "Saturday"
#else:
#    dayOfWeek = "Sunday"