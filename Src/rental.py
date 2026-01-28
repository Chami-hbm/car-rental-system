from database import DatabaseManager
from datetime import datetime, timedelta


class RentalManager:
    def __init__(self):
        self.db = DatabaseManager()

    def is_car_available(self, car_id, start_date, end_date):
        check_query = """
            SELECT id, start_date, end_date 
            FROM rentals 
            WHERE car_id = %s 
            AND status IN ('pending', 'approved')
            AND (
                (start_date <= %s AND end_date >= %s) OR   -- Existing rental starts before new end and ends after new start
                (start_date <= %s AND end_date >= %s) OR   -- Existing rental starts before new start and ends after new start
                (start_date >= %s AND end_date <= %s)      -- New rental completely overlaps existing
            )
        """
        cursor = self.db.execute_query(check_query, (
            car_id,
            end_date, start_date,  # First condition
            start_date, start_date,  # Second condition
            start_date, end_date  # Third condition
        ))
        return cursor.fetchone() is None

    def calculate_price(self, daily_price, days, user):
        base_price = float(daily_price)
        discount_percent = 0

        if user.rentals_count > 0 and user.last_rental_date:
            days_since_last = (datetime.today().date() - user.last_rental_date).days
            if days_since_last <= 30:
                discount_percent = 5

        discount_factor = 1 - (discount_percent / 100)
        total_price = round(base_price * days * discount_factor, 2)
        return total_price, discount_percent

    def create_rental(self, user_id, car_id, start_date, end_date, total_price):
        # First create the rental
        query = """INSERT INTO rentals 
                (user_id, car_id, start_date, end_date, status, total_price)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        self.db.execute_query(query, (user_id, car_id, start_date, end_date, 'pending', total_price))

        # Then update user's rental count and last rental date
        update_query = """
            UPDATE users 
            SET rentals_count = rentals_count + 1,
                last_rental_date = %s 
            WHERE id = %s
        """
        self.db.execute_query(update_query, (end_date, user_id))