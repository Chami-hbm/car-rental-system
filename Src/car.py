from database import DatabaseManager


class Car:
    def __init__(self, car_id, make, model, year, daily_price, min_rent, max_rent, available):
        self.id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.daily_price = daily_price
        self.min_rent = min_rent
        self.max_rent = max_rent
        self.available = available


class CarManager:
    def __init__(self):
        self.db = DatabaseManager()

    def add_car(self, make, model, year, daily_price, min_rent, max_rent):
        query = """INSERT INTO cars 
                   (make, model, year, daily_price, min_rent, max_rent)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        self.db.execute_query(query, (make, model, year, daily_price, min_rent, max_rent))
        print("Car added successfully!")

    def get_available_cars(self):
        query = "SELECT * FROM cars WHERE available = TRUE"
        cursor = self.db.execute_query(query)
        return [Car(*row) for row in cursor.fetchall()]

    def get_all_cars(self):
        query = "SELECT * FROM cars"
        cursor = self.db.execute_query(query)
        return [Car(*row) for row in cursor.fetchall()]

    def edit_car(self, car_id, **kwargs):
        set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(car_id)

        query = f"UPDATE cars SET {set_clause} WHERE id = %s"
        self.db.execute_query(query, values)
        print("Car updated successfully!")

    def delete_car(self, car_id):
        # Check for active rentals first
        check_query = "SELECT id FROM rentals WHERE car_id = %s AND status IN ('pending', 'approved')"
        cursor = self.db.execute_query(check_query, (car_id,))

        if cursor.fetchone():
            print("Cannot delete car with active/pending rentals!")
            return False

        delete_query = "DELETE FROM cars WHERE id = %s"
        self.db.execute_query(delete_query, (car_id,))
        print("Car deleted successfully!")
        return True