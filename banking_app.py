# Task 03: Banking Console Application
# Kiran Academy - Java & Python Programming Task

# fixed opening balance
balance = 10000

print("Welcome to Kiran Bank")
print("Opening Balance: ₹" + str(balance))

while True:
    # show the menu
    print()
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        # check balance
        print("Current Balance: ₹" + str(balance))

    elif choice == "2":
        # deposit money
        try:
            amount = float(input("Enter deposit amount: "))
        except ValueError:
            print("Invalid input: Please enter a number.")
            continue

        if amount <= 0:
            print("Invalid amount: Deposit must be greater than ₹0.")
        else:
            balance = balance + amount
            print("Deposit successful.")
            print("Updated Balance: ₹" + str(balance))

    elif choice == "3":
        # withdraw money
        try:
            amount = float(input("Enter withdrawal amount: "))
        except ValueError:
            print("Invalid input: Please enter a number.")
            continue

        if amount <= 0:
            print("Invalid amount: Withdrawal must be greater than ₹0.")
        elif amount > balance:
            print("Transaction failed: Insufficient balance.")
            print("Current Balance: ₹" + str(balance))
        else:
            balance = balance - amount
            print("Withdrawal successful.")
            print("Updated Balance: ₹" + str(balance))

    elif choice == "4":
        # exit
        print("Thank you for banking with us. Goodbye!")
        break

    else:
        print("Invalid choice: Please enter 1, 2, 3 or 4.")
