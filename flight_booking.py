"""
Kiran Academy - Task 04: Flight Booking Console Application (OOP)

OOP concepts demonstrated:
  * Class & Object  : Flight, Passenger, Booking, FlightBookingSystem
  * Encapsulation   : private attributes + controlled access via properties/methods
  * Inheritance     : RegularPassenger and StudentPassenger extend Passenger
  * Polymorphism    : get_discount_percentage() behaves differently per passenger type
  * Abstraction     : Passenger is an Abstract Base Class (ABC) defining the discount contract
"""

from abc import ABC, abstractmethod

CURRENCY = "\u20b9"  # Indian Rupee symbol


# ----------------------------------------------------------------------------
# Flight
# ----------------------------------------------------------------------------
class Flight:
    """Represents a flight. Seat count can only be changed through methods."""

    def __init__(self, code, airline, source, destination, seats, base_fare):
        self.__code = code
        self.__airline = airline
        self.__source = source
        self.__destination = destination
        self.__available_seats = seats
        self.__base_fare = base_fare

    # Read-only access (getters)
    @property
    def code(self):
        return self.__code

    @property
    def airline(self):
        return self.__airline

    @property
    def source(self):
        return self.__source

    @property
    def destination(self):
        return self.__destination

    @property
    def available_seats(self):
        return self.__available_seats

    @property
    def base_fare(self):
        return self.__base_fare

    def has_seats(self, count):
        return 0 < count <= self.__available_seats

    def reserve_seats(self, count):
        """Reduce available seats. Returns True only if the reservation succeeded."""
        if not self.has_seats(count):
            return False
        self.__available_seats -= count
        return True

    def route(self):
        return f"{self.__source} to {self.__destination}"

    def __str__(self):
        return (f"{self.__code:<8}{self.__airline:<14}{self.__source:<12}"
                f"{self.__destination:<12}{self.__available_seats:<8}"
                f"{CURRENCY}{self.__base_fare:,.0f}")


# ----------------------------------------------------------------------------
# Passenger hierarchy (Abstraction + Inheritance + Polymorphism)
# ----------------------------------------------------------------------------
class Passenger(ABC):
    """Abstract base class: every passenger type must define its own discount."""

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @abstractmethod
    def get_discount_percentage(self):
        """Return discount as a percentage (e.g. 10 for 10%)."""

    @abstractmethod
    def get_type_name(self):
        """Return passenger category name for display."""

    def calculate_discount(self, subtotal):
        # Same call works for every subclass -> polymorphism
        return subtotal * self.get_discount_percentage() / 100


class RegularPassenger(Passenger):
    def get_discount_percentage(self):
        return 0

    def get_type_name(self):
        return "Regular"


class StudentPassenger(Passenger):
    def get_discount_percentage(self):
        return 10

    def get_type_name(self):
        return "Student"


# ----------------------------------------------------------------------------
# Booking
# ----------------------------------------------------------------------------
class Booking:
    """Immutable record of a confirmed booking."""

    def __init__(self, booking_id, flight, passenger, tickets,
                 subtotal, discount, final_amount):
        self.__booking_id = booking_id
        self.__flight = flight
        self.__passenger = passenger
        self.__tickets = tickets
        self.__subtotal = subtotal
        self.__discount = discount
        self.__final_amount = final_amount

    @property
    def booking_id(self):
        return self.__booking_id

    @property
    def flight(self):
        return self.__flight

    @property
    def passenger(self):
        return self.__passenger

    @property
    def tickets(self):
        return self.__tickets

    @property
    def subtotal(self):
        return self.__subtotal

    @property
    def discount(self):
        return self.__discount

    @property
    def final_amount(self):
        return self.__final_amount


# ----------------------------------------------------------------------------
# Flight Booking System (controller)
# ----------------------------------------------------------------------------
class FlightBookingSystem:
    PASSENGER_TYPES = {"regular": RegularPassenger, "student": StudentPassenger}

    def __init__(self):
        self.__flights = [
            Flight("PN101", "Kiran Air", "Pune", "Delhi", 20, 4000),
            Flight("MB202", "Kiran Air", "Mumbai", "Bengaluru", 15, 3500),
            Flight("PH303", "SkyJet", "Pune", "Hyderabad", 10, 2800),
            Flight("DC404", "SkyJet", "Delhi", "Chennai", 25, 5200),
        ]
        self.__bookings = []
        self.__next_booking_number = 1001

    # ---- Display flights ---------------------------------------------------
    def display_flights(self):
        print("\n" + "-" * 70)
        print(f"{'Code':<8}{'Airline':<14}{'From':<12}{'To':<12}{'Seats':<8}Base Fare")
        print("-" * 70)
        for flight in self.__flights:
            print(flight)
        print("-" * 70)

    # ---- Find flight -------------------------------------------------------
    def find_flight(self, code):
        code = code.strip().upper()
        for flight in self.__flights:
            if flight.code == code:
                return flight
        return None

    # ---- Validation --------------------------------------------------------
    def validate_booking_details(self, code, name, age_text, type_text, tickets_text):
        """
        Validate all raw inputs.
        Returns (error_message, data). If error_message is None, data holds the
        cleaned values: (flight, name, age, passenger_class, tickets).
        """
        flight = self.find_flight(code)
        if flight is None:
            return "Invalid flight code.", None

        name = name.strip()
        if not name:
            return "Passenger name cannot be blank.", None

        try:
            age = int(age_text.strip())
        except ValueError:
            return "Age must be a whole number.", None
        if age <= 0:
            return "Age must be greater than 0.", None

        passenger_class = self.PASSENGER_TYPES.get(type_text.strip().lower())
        if passenger_class is None:
            return "Passenger type must be Regular or Student.", None

        try:
            tickets = int(tickets_text.strip())
        except ValueError:
            return "Number of tickets must be a whole number.", None
        if tickets <= 0:
            return "Number of tickets must be greater than 0.", None

        if not flight.has_seats(tickets):
            return "Not enough seats available.", None

        return None, (flight, name, age, passenger_class, tickets)

    # ---- Fare --------------------------------------------------------------
    def calculate_fare(self, flight, passenger, tickets):
        """Returns (subtotal, discount, final_amount)."""
        subtotal = flight.base_fare * tickets
        discount = passenger.calculate_discount(subtotal)  # polymorphic call
        return subtotal, discount, subtotal - discount

    # ---- Confirm booking ---------------------------------------------------
    def confirm_booking(self, flight, passenger, tickets):
        subtotal, discount, final_amount = self.calculate_fare(flight, passenger, tickets)

        if not flight.reserve_seats(tickets):   # seats change only here, via Flight
            return None

        booking_id = f"BK{self.__next_booking_number}"
        self.__next_booking_number += 1
        booking = Booking(booking_id, flight, passenger, tickets,
                          subtotal, discount, final_amount)
        self.__bookings.append(booking)
        return booking

    # ---- Summary -----------------------------------------------------------
    def display_summary(self, booking):
        p = booking.passenger
        f = booking.flight
        print(f"Booking ID: {booking.booking_id}")
        print(f"Flight: {f.code} | {f.route()} ({f.airline})")
        print(f"Passenger: {p.name} (Age: {p.age})")
        print(f"Passenger type: {p.get_type_name()}")
        print(f"Tickets: {booking.tickets}")
        print(f"Base fare per ticket: {CURRENCY}{f.base_fare:,.0f}")
        print(f"Subtotal: {CURRENCY}{booking.subtotal:,.0f}")
        print(f"{p.get_type_name()} discount ({p.get_discount_percentage()}%): "
              f"{CURRENCY}{booking.discount:,.0f}")
        print(f"Final amount: {CURRENCY}{booking.final_amount:,.0f}")

    # ---- Menu actions ------------------------------------------------------
    def book_flight(self):
        code = input("Enter flight code: ")
        name = input("Enter passenger name: ")
        age_text = input("Enter age: ")
        type_text = input("Passenger type (Regular/Student): ")
        tickets_text = input("Enter number of tickets: ")

        error, data = self.validate_booking_details(
            code, name, age_text, type_text, tickets_text)
        if error:
            print(f"\nBooking failed: {error}")
            print("No booking was created. Available seats remain unchanged.")
            return

        flight, name, age, passenger_class, tickets = data
        passenger = passenger_class(name, age)
        booking = self.confirm_booking(flight, passenger, tickets)

        if booking is None:
            print("\nBooking failed: Not enough seats available.")
            print("No booking was created. Available seats remain unchanged.")
            return

        print("\nBooking confirmed!")
        self.display_summary(booking)

    def view_booking(self):
        if not self.__bookings:
            print("\nNo bookings yet. Choose 'Book Flight' to make your first booking.")
            return
        print("\nMost recent booking:")
        self.display_summary(self.__bookings[-1])

    # ---- Main loop ---------------------------------------------------------
    def run(self):
        while True:
            print("\nWelcome to Kiran Air Booking")
            print("1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.display_flights()
            elif choice == "2":
                self.book_flight()
            elif choice == "3":
                self.view_booking()
            elif choice == "4":
                print("Thank you for using Kiran Air Booking!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    FlightBookingSystem().run()
