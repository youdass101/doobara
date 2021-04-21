
annual_salary = float(input("Enter your annual salary:"))

portion_saved = 0
total_cost = 1000000
epsilon = 100
counter = 0
semi_annual_raise = 0.7
portion_down_payment = total_cost * 0.25
current_savings = 0 
monthly_salary = annual_salary / 12
months = 0 
r = 0.04
low = 0
high = 10000
guess = int((high+low)/2)

print("first guess", guess)

while abs(current_savings - portion_down_payment) >= epsilon:
    current_savings = 0
    months = 0
    guess = float(guess / 10000)
    print(guess)
    # CALACULATE THE GUESS
    while months < 36:

        # RAISE CACULATE
        if months > 0 and months % 6 == 0:
            monthly_salary += monthly_salary * semi_annual_raise
        current_savings += (current_savings * r)/12
        months += 1
        current_savings += monthly_salary * guess
        current_savings = int(current_savings)
        
    
    if current_savings < portion_down_payment:
        low = int(guess * 10000)
    else:
        high = int(guess * 10000)
    guess = int((high + low)/2)
    counter += 1
    if guess == 0:
        break
    print(current_savings)





print("rate is:",guess)
