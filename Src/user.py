from database import DatabaseManager
import bcrypt

class User:
    def __init__(self, user_id, username, role, rentals_count, last_rental_date):
        self.id = user_id
        self.username = username
        self.role = role
        self.rentals_count = rentals_count
        self.last_rental_date = last_rental_date


class Customer(User):
    def __init__(self, user_id, username, rentals_count, last_rental_date):
        super().__init__(user_id, username, 'customer', rentals_count, last_rental_date)

class Admin(User):
    def __init__(self, user_id, username, rentals_count, last_rental_date):
        super().__init__(user_id, username, 'admin', rentals_count, last_rental_date)


class UserManager:
    def __init__(self):
        self.db = DatabaseManager()

    def register(self, username, password, role):
        # Hash password with salt
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (username, hashed_pw.decode(), role))
        print("Registration successful!")

    def login(self, username, password):
        query = """
            SELECT id, role, rentals_count, last_rental_date, password 
            FROM users 
            WHERE username = %s
        """
        cursor = self.db.execute_query(query, (username,))

        if not cursor:
            return None

        result = cursor.fetchone()

        if result:
            user_id, role, rentals_count, last_rental_date, stored_pw = result

            # Verify password against stored hash
            if bcrypt.checkpw(password.encode(), stored_pw.encode()):
                if role == 'admin':
                    return Admin(int(user_id), username, int(rentals_count), last_rental_date)
                else:
                    return Customer(int(user_id), username, int(rentals_count), last_rental_date)
        return None
