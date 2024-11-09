import unittest
from appium import webdriver
import sqlite3


class DatabaseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Appium driver
        capabilities = {
            "platformName": 'Android',
            "deviceName": '146ce6c8',
            "app": r'C:\Users\20115\Downloads\app-release.apk'
        }
        cls.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', capabilities)
        cls.driver.implicitly_wait(50)

        # Set up database connection (assuming SQLite for example)
        cls.conn = sqlite3.connect('test_database.db')
        cls.cursor = cls.conn.cursor()

    def test_user_data_inserted_into_db(self):
        # Register a user
        self.register_user("test_user", "testuser@example.com", "ValidPassword123")

        # Query the database to check if the user exists
        self.cursor.execute("SELECT * FROM users WHERE email = ?", ("testuser@example.com",))
        user = self.cursor.fetchone()

        self.assertIsNotNone(user, "User data was not inserted correctly into the database.")
        self.assertEqual(user[1], "test_user", "Username mismatch.")
        self.assertEqual(user[2], "testuser@example.com", "Email mismatch.")

    def test_duplicate_registration_prevention(self):
        # Register a user with the same email
        self.register_user("duplicate_user", "duplicate@example.com", "ValidPassword123")

        # Try to register again with the same email
        self.register_user("duplicate_user2", "duplicate@example.com", "ValidPassword123")

        # Query the database to check if the second registration failed
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", ("duplicate@example.com",))
        count = self.cursor.fetchone()[0]

        self.assertEqual(count, 1, "Duplicate registration was allowed.")

    def test_database_connection_error_handling(self):
        # Simulate a database connection error by closing the connection
        self.conn.close()

        try:
            self.register_user("error_user", "error@example.com", "ValidPassword123")
            self.fail("Database connection error was not handled correctly.")
        except Exception as e:
            self.assertTrue("Database connection error" in str(e), "Error message mismatch.")

    def register_user(self, username, email, password):
        # Helper function to register a user (simulated, assuming success)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]').send_keys(username)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Email"]').send_keys(email)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Password"]').send_keys(password)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.conn.close()


if __name__ == "__main__":
    unittest.main()
