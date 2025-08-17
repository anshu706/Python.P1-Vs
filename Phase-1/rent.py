# Inputs we need from the user
# Total rent
# Total food ordered for snacking
# Electricity units spend
# Charge per unit
# Persons living in flat

# Output
# Total amount you've to pay is

rent = int(input("Enter your flat rent = "))
food = int(input("Enter the amount of food ordered = "))
electricity_spend = int(input("Enter the total of electricity spend = "))
charge_per_unit = int(input("Enter the charge per unit = "))
persons = int(input("Enter the number of persons living in flat = "))

total_bill = electricity_spend * charge_per_unit

output = (food + rent + total_bill) / persons

print("Each person will pay = ", output)
