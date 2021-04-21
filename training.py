
annual_salary = float(input("Enter the starting salary:"))

total_cost = 1000000
epsilon = 100
counter = 0
semi_annual_raise = 0.07
portion_down_payment = total_cost * 0.25
current_savings = 0 
r = 0.04
low = 0
high = 10000
guess = int((high+low)/2)
p_guess = 0
fail = 0

while abs(current_savings - portion_down_payment) >= epsilon:
    current_savings = 0
    months = 0
    monthly_salary = 0
    guess = float(guess / 10000)
    monthly_salary = annual_salary / 12
    if guess == p_guess:
        print("It is not possible to pay the down payment in three years")
        fail = 1
        break

    # CALACULATE THE GUESS
    while months < 36:
        # RAISE CACULATE
        if months > 0 and months % 6 == 0:
            monthly_salary += monthly_salary * semi_annual_raise
        current_savings += (current_savings * r)/12
        months += 1
        current_savings += monthly_salary * guess
    
    if current_savings < portion_down_payment:
        low = int(guess * 10000)
    else:
        high = int(guess * 10000)
    p_guess = guess
    guess = int((high + low)/2)
    counter += 1

if fail != 1:
    print("Best savings rate: %.4f" % (guess/10000))
    print("Steps in bisection search:", counter)
