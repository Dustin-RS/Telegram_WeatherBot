import sqlite3


class DataBaseHelper:
    """
    Class which is providing access to database.
    """
    def __init__(self, database_file):
        """
        Connecting to database and keep cursor.
        """
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_user_city(self, user_id):
        """
        Get user's city column.
        """
        with self.connection:
            result = self.cursor.execute("SELECT city FROM CityHistory WHERE user_id = ?", (user_id,)).fetchall()
            return str(result[0][0])

    def user_exists(self, user_id):
        """
        Check if the user already exists in database.
        """
        with self.connection:
            result = self.cursor.execute("SELECT * FROM CityHistory WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, city="Moscow"):
        """
        Adding new user to database.
        """
        with self.connection:
            return self.cursor.execute("INSERT INTO 'CityHistory' ('user_id', 'city') VALUES (?,?)", (user_id, city))

    def update_user(self, user_id, city):
        """
        Change user's home city column.
        """
        with self.connection:
            return self.cursor.execute("UPDATE CityHistory SET city = ? WHERE user_id = ?", (city, user_id))

    def close(self):
        """
        Closing conntection with database.
        """
        self.connection.close()
