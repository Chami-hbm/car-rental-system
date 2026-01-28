import sys
from database import DatabaseManager
from user import UserManager, Customer, Admin
from car import CarManager, Car
from rental import RentalManager
from datetime import datetime
import stdiomask

class CarRentalCLI:
    def __init__(self):
        self.user_manager = UserManager()
        self.car_manager = CarManager()
        self.rental_manager = RentalManager()
        self.current_user = None

    def start(self):
        while True:
            print("\nWelcome to MC Car Rental System")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                sys.exit()
            else:
                print("Invalid choice!")

    def register(self):
        username = input("Enter username: ")
        password = stdiomask.getpass("Password: ", mask='*')
        role = input("Enter role (admin/customer): ").lower()
        self.user_manager.register(username, password, role)

    def login(self):
        username = input("Username: ")
        password = stdiomask.getpass("Password: ", mask='*')
        user = self.user_manager.login(username, password)
        if user:
            self.current_user = user
            self.show_role_menu()
        else:
            print("Invalid credentials!")

    def show_role_menu(self):
        if isinstance(self.current_user, Admin):
            self.admin_menu()
        else:
            self.customer_menu()

    # ------------ ADMIN MENU ------------
    def admin_menu(self):
        while True:
            print("\nAdmin Menu - MC Car Rentals")
            print("1. Add Car")
            print("2. Edit Car")
            print("3. Delete Car")
            print("4. View Rentals")
            print("5. Manage Bookings")
            print("6. Logout")
            choice = input("Enter choice: ")

            if choice == '1':
                self.add_car()
            elif choice == '2':
                self.edit_car()
            elif choice == '3':
                self.delete_car()
            elif choice == '4':
                self.view_rentals()
            elif choice == '5':
                self.manage_bookings()
            elif choice == '6':
                print("Thank you for using MC Car Rentals!")
                self.current_user = None
                return
            else:
                print("Invalid choice!")

    def add_car(self):
        try:
            make = input("Make: ")
            model = input("Model: ")
            year = int(input("Year: "))
            daily_price = float(input("Daily price: "))
            min_rent = int(input("Minimum rent days: "))
            max_rent = int(input("Maximum rent days: "))
            self.car_manager.add_car(make, model, year, daily_price, min_rent, max_rent)
        except ValueError:
            print("Invalid input! Please enter numbers where required.")

    def edit_car(self):
        try:
            cars = self.car_manager.get_all_cars()
            print("\nAvailable Cars:")
            for car in cars:
                print(f"{car.id}: {car.make} {car.model}")

            car_id = int(input("Enter car ID to edit: "))
            print("\nLeave blank to keep current value")

            updates = {}
            fields = {
                'make': input("New make: "),
                'model': input("New model: "),
                'year': input("New year: "),
                'daily_price': input("New daily price: "),
                'min_rent': input("New minimum rent days: "),
                'max_rent': input("New maximum rent days: ")
            }

            for key, value in fields.items():
                if value.strip():
                    if key in ['year', 'min_rent', 'max_rent']:
                        updates[key] = int(value)
                    elif key == 'daily_price':
                        updates[key] = float(value)
                    else:
                        updates[key] = value

            if updates:
                self.car_manager.edit_car(car_id, **updates)
            else:
                print("No changes made!")

        except ValueError:
            print("Invalid input format!")

    def delete_car(self):
        try:
            cars = self.car_manager.get_all_cars()
            print("\nAvailable Cars:")
            for car in cars:
                print(f"{car.id}: {car.make} {car.model}")

            car_id = int(input("Enter car ID to delete: "))
            confirm = input(f"Are you sure you want to delete car {car_id}? (y/n): ").lower()

            if confirm == 'y':
                self.car_manager.delete_car(car_id)
            else:
                print("Deletion cancelled")

        except ValueError:
            print("Invalid car ID format!")

    def view_rentals(self):
        query = "SELECT * FROM rentals"
        cursor = DatabaseManager().execute_query(query)
        rentals = cursor.fetchall()
        print("\nAll Rentals:")
        for rental in rentals:
            print(f"ID: {rental[0]}, Car: {rental[2]}, Start Date: {rental[3]}, Ends on: {rental[4]} Status: {rental[5]}")

    def manage_bookings(self):
        rental_id = input("Enter rental ID to manage: ")
        print("1. Approve")
        print("2. Reject")
        action = input("Choose action: ")

        if action == '1':
            status = 'approved'
        elif action == '2':
            status = 'rejected'
        else:
            print("Invalid choice!")
            return

        query = "UPDATE rentals SET status = %s WHERE id = %s"
        DatabaseManager().execute_query(query, (status, rental_id))
        print("Booking status updated!")

    # ------------ CUSTOMER MENU ------------
    def customer_menu(self):
        while True:
            print("\nCustomer Menu - MC Car Rentals")
            print("1. View Available Cars")
            print("2. Rent Car")
            print("3. Logout")
            choice = input("Enter choice: ")

            if choice == '1':
                self.view_available_cars()
            elif choice == '2':
                self.handle_rental()
            elif choice == '3':
                print("Thank you for using MC Car Rentals!")
                self.current_user = None
                return
            else:
                print("Invalid choice!")

    def view_available_cars(self):
        cars = self.car_manager.get_available_cars()
        if not cars:
            print("No cars available!")
            return

        print("\nAvailable Cars:")
        for car in cars:
            print(f"{car.id}: {car.make} {car.model} ({car.year}) - ${car.daily_price}/day")

    def handle_rental(self):
        try:
            car_id = int(input("Enter car ID: "))
            car = self.get_car_by_id(car_id)  # Check car first before dates

            if not car:
                print("Invalid car ID!")
                return

            # Get dates after confirming car exists
            today = datetime.today().date()

            start_date = datetime.strptime(input("Start date (YYYY-MM-DD): "),"%Y-%m-%d").date()

            if start_date < today:
                print("Error: Start date cannot be in the past")
                return

            end_date = datetime.strptime(input("End date (YYYY-MM-DD): "),"%Y-%m-%d").date()

            if end_date <= start_date:
                print("Error: End date must be after start date")
                return
            days = (end_date - start_date).days

            # Validate all conditions
            if days < car.min_rent:
                print(f"Minimum rental period for {car.make} {car.model} is {car.min_rent} days")
                return
            if days > car.max_rent:
                print(f"Maximum rental period for {car.make} {car.model} is {car.max_rent} days")
                return

            # Check for overlapping rentals
            if not self.rental_manager.is_car_available(car.id, start_date, end_date):
                # Get conflicting rentals for detailed message
                conflict_query = """
                    SELECT start_date, end_date 
                    FROM rentals 
                    WHERE car_id = %s 
                    AND status IN ('pending', 'approved')
                    AND ((start_date <= %s AND end_date >= %s) 
                        OR (start_date <= %s AND end_date >= %s) 
                        OR (start_date >= %s AND end_date <= %s))
                """
                cursor = DatabaseManager().execute_query(conflict_query, (
                    car.id,
                    end_date, start_date,  # First condition
                    start_date, start_date,  # Second condition
                    start_date, end_date  # Third condition
                ))

                print("\n❌ Car not available for selected dates. Conflicting rentals:")
                for start, end in cursor.fetchall():
                    print(f"  - {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
                return


            # Calculate price with loyalty discount
            total_price, discount_percent = self.rental_manager.calculate_price(
                car.daily_price, days, self.current_user
            )

            # Create rental
            self.rental_manager.create_rental(
                self.current_user.id, car_id,
                start_date.isoformat(),
                end_date.isoformat(),
                total_price
            )
            # Display price breakdown
            if discount_percent > 0:
                original_price = float(car.daily_price) * days
                discount_amount = original_price - total_price
                print(f"\n✅ Rental Created!")
                print(f"📅 Period: {start_date} to {end_date} ({days} days)")
                print(f"💵 Base price: ${original_price:.2f}")
                print(f"🎫 Loyalty discount ({discount_percent}%): -${discount_amount:.2f}")
                print(f"💳 Total price: ${total_price:.2f}")
            else:
                print(f"\n✅ Rental Created! Total price: ${total_price:.2f}")

        except ValueError as e:
            print(f"Invalid input: {e}")

    def get_car_by_id(self, car_id):
        query = "SELECT * FROM cars WHERE id = %s"
        cursor = DatabaseManager().execute_query(query, (car_id,))
        result = cursor.fetchone()
        if result:
            return Car(*result)
        return None


if __name__ == "__main__":
    cli = CarRentalCLI()
    cli.start()