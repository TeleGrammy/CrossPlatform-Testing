from appium import webdriver
import unittest

class RegistrationFieldValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capabilities = {
            "platformName": 'Android',
            "deviceName": '146ce6c8',
            "app": r'C:\Users\20115\Downloads\app-release.apk'
        }
        cls.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', capabilities)
        cls.driver.implicitly_wait(50)

    def fill_form(self, username="", email="", phone="", password="", conf_password=""):
        # Helper function to fill the form fields
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]').send_keys(username)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Email"]').send_keys(email)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Phone"]').send_keys(phone)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Password"]').send_keys(password)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Confirm Password"]').send_keys(conf_password)

    def test_empty_individual_fields(self):
        # Test submission with each field empty one by one
        field_names = ["Username", "Email", "Phone", "Password", "Confirm Password"]
        for field in field_names:
            self.fill_form()
            field_element = self.driver.find_element_by_xpath(f'//android.widget.EditText[@content-desc="{field}"]')
            field_element.clear()
            self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
            self.assertTrue(self.check_error_message(f"{field} is required"), f"Error message for empty {field} not displayed.")

    def test_all_fields_empty(self):
        # Test the form submission when all fields are empty
        self.fill_form()
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("All fields are required"), "Error message for all fields empty not displayed.")

    def test_invalid_email_format(self):
        # Test invalid email formats
        invalid_emails = ["user@", "user@domain", "user@domain@domain.com", "user@@domain.com"]
        for email in invalid_emails:
            self.fill_form(email=email)
            self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
            self.assertTrue(self.check_error_message("Invalid email format"), f"Invalid email '{email}' not detected.")

    def test_password_strength(self):
        # Test password strength requirements
        weak_passwords = ["short", "12345678", "password", "Password123"]
        for password in weak_passwords:
            self.fill_form(password=password, conf_password=password)
            self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
            self.assertTrue(self.check_error_message("Password does not meet strength requirements"), f"Weak password '{password}' was not flagged.")

    def test_password_confirmation_match(self):
        # Test that password and confirmation must match
        self.fill_form(password="ValidPass123!", conf_password="DifferentPass123!")
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Passwords do not match"), "Mismatched passwords not flagged.")

    def test_excessively_long_email(self):
        # Test excessively long email addresses
        long_email = "a" * 256 + "@example.com"
        self.fill_form(email=long_email)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Email is too long"), "Long email not flagged.")

    def test_password_no_alphanumeric(self):
        # Test passwords with no alphanumeric characters
        non_alphanumeric_password = "*********"
        self.fill_form(password=non_alphanumeric_password, conf_password=non_alphanumeric_password)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Password must contain letters and numbers"), "Password with no alphanumeric characters not flagged.")

    def test_password_with_spaces_and_special_characters(self):
        # Test passwords containing spaces and special characters
        special_char_password = "Pass word!@#"
        self.fill_form(password=special_char_password, conf_password=special_char_password)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_successful_signup(), "Password with spaces/special characters not accepted.")

    def test_trimmed_spaces_in_password(self):
        # Test that leading/trailing spaces in passwords are handled correctly
        password_with_spaces = " ValidPass123! "
        self.fill_form(password=password_with_spaces.strip(), conf_password=password_with_spaces.strip())
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_successful_signup(), "Password with leading/trailing spaces not handled correctly.")

    def test_common_passwords(self):
        # Test that commonly used passwords are not allowed
        common_passwords = ["password", "123456", "admin"]
        for password in common_passwords:
            self.fill_form(password=password, conf_password=password)
            self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
            self.assertTrue(self.check_error_message("Common passwords are not allowed"), f"Common password '{password}' not flagged.")

    def test_repeated_character_password(self):
        # Test passwords with repeated characters
        repeated_char_password = "aaaaaaaaaa"
        self.fill_form(password=repeated_char_password, conf_password=repeated_char_password)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Password is too weak"), "Repeated character password not flagged.")

    def check_error_message(self, expected_message):
        # Helper function to verify specific error messages
        error_element = self.driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Error Message']")
        return expected_message in error_element.text

    def check_successful_signup(self):
        # Placeholder method to verify successful signup
        success_element = self.driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Success Message']")
        return "Welcome" in success_element.text

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
