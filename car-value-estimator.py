print("Car Value Estimator")

make = input("Enter car make: ")
model = input("Enter car model: ")

purchase_price = float(input("Enter original price: "))
age = int(input("Enter age of car in years: "))
miles = int(input("Enter mileage: "))

value = purchase_price

for i in range(age):
    value = value * 0.90

value = value - (miles * 0.05)

if value < 0:
    value = 0

print()
print("----- Results -----")
print("Car:", make, model)
print("Estimated Value: $", round(value, 2))