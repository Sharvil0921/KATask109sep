# Task 02 - Cab Booking Chatbot
import random

# predefined cab rates (per km)
auto_rate = 12
sedan_rate = 18
suv_rate = 25

# predefined routes
route1_source = "Pune Station"
route1_dest = "Shivajinagar"
route1_km = 5

route2_source = "Swargate"
route2_dest = "Kothrud"
route2_km = 8

route3_source = "Hinjawadi"
route3_dest = "Wakad"
route3_km = 10

print("Welcome to Cab Booking Chatbot")

while True:
    print("\n----- MAIN MENU -----")
    print("1. Book Ride")
    print("2. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        # choose cab type
        print("\nChoose Cab Type")
        print("1. Auto")
        print("2. Sedan")
        print("3. SUV")
        cab_choice = input("Enter cab choice: ")

        if cab_choice == "1":
            cab_name = "Auto"
            rate = auto_rate
        elif cab_choice == "2":
            cab_name = "Sedan"
            rate = sedan_rate
        elif cab_choice == "3":
            cab_name = "SUV"
            rate = suv_rate
        else:
            print("Invalid cab choice! Try again.")
            continue

        # choose route
        print("\nChoose Route")
        print("1.", route1_source, "to", route1_dest, "-", route1_km, "km")
        print("2.", route2_source, "to", route2_dest, "-", route2_km, "km")
        print("3.", route3_source, "to", route3_dest, "-", route3_km, "km")
        route_choice = input("Enter route number: ")

        if route_choice == "1":
            source = route1_source
            destination = route1_dest
            distance = route1_km
        elif route_choice == "2":
            source = route2_source
            destination = route2_dest
            distance = route2_km
        elif route_choice == "3":
            source = route3_source
            destination = route3_dest
            distance = route3_km
        else:
            print("Invalid route choice! Try again.")
            continue

        # calculate fare
        fare = rate * distance

        print("\n----- RIDE DETAILS -----")
        print("Cab Type    :", cab_name)
        print("Source      :", source)
        print("Destination :", destination)
        print("Distance    :", distance, "km")
        print("Rate        : Rs", rate, "per km")
        print("Total Fare  : Rs", fare)

        # confirm or cancel (only possible before OTP)
        print("\n1. Confirm & Share OTP")
        print("2. Cancel Ride")
        confirm = input("Enter your choice: ")

        if confirm == "1":
            otp = random.randint(1000, 9999)
            print("\nYour OTP is:", otp)
            print("OTP has been shared. Ride cannot be cancelled now.")
            print("Booking confirmed! Your", cab_name, "is on the way.")
        elif confirm == "2":
            print("Ride cancelled. No OTP was shared.")
        else:
            print("Invalid choice! Ride not booked.")

    elif choice == "2":
        print("Thank you for using Cab Booking Chatbot. Goodbye!")
        break

    else:
        print("Invalid choice! Please enter 1 or 2.")
