from appium import webdriver
import unittest

class RegistrationErrorHandlingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capabilities = {
            "platformName": 'Android',
            "deviceName": '146ce6c8',
            "app": r'C:\Users\20115\Downloads\app-release.apk'
        }
        cls.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', capabilities)
        cls.driver.implicitly_wait(50)

    def fill_form(self, username="testuser", email="testuser@example.com", phone="1234567890", password="StrongPass123!", conf_password="StrongPass123!"):
        # Helper function to fill the form fields
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]').send_keys(username)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Email"]').send_keys(email)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Phone"]').send_keys(phone)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Password"]').send_keys(password)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Confirm Password"]').send_keys(conf_password)

    def test_existing_email_error(self):
        # Check error when using an already registered email
        self.fill_form(email="existinguser@example.com")
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Email already registered"), "Duplicate email error not displayed.")

    def test_captcha_verification(self):
        # Verify CAPTCHA functionality, placeholder for CAPTCHA interaction
        self.fill_form()
        self.solve_captcha()
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_successful_signup(), "CAPTCHA verification failed or user flagged as bot.")

    def test_user_friendly_error_messages(self):
        # Test that errors are user-friendly for various issues
        self.fill_form(email="invalidemail@", password="weakpass", conf_password="diffpass")
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Invalid email format"), "Invalid email error message not user-friendly.")
        self.assertTrue(self.check_error_message("Password does not meet criteria"), "Password strength error message not user-friendly.")
        self.assertTrue(self.check_error_message("Passwords do not match"), "Password mismatch error message not user-friendly.")

    def test_existing_username_error(self):
        # Check error when using a taken username
        self.fill_form(username="existinguser")
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Username already taken"), "Duplicate username error not displayed.")

    def test_internal_server_error_handling(self):
        # Simulate internal server error and ensure user-friendly message is shown
        self.fill_form(username="testuser", email="testuser@example.com")
        self.simulate_server_error()
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("An unexpected error occurred. Please try again later."), "Server error message not user-friendly.")

    def test_high_traffic_handling(self):
        # Test registration under high server traffic or slow response
        self.fill_form(username="testuser", email="testuser@example.com")
        self.simulate_high_traffic()
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("High traffic, please try again shortly."), "High traffic error message not displayed correctly.")

    def test_context_specific_error_messages(self):
        # Verify context-specific error messages for different cases
        self.fill_form(username="existinguser", email="invalidemail@")
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Username already taken"), "Username taken error message not specific.")
        self.assertTrue(self.check_error_message("Invalid email format"), "Invalid email format error message not specific.")

    def test_locked_account_restriction(self):
        # Ensure user with a locked account receives account recovery instructions
        self.fill_form(username="lockeduser")
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Account locked. Please follow account recovery steps."), "Locked account error message not user-friendly.")

    def test_reserved_keyword_username(self):
        # Prevent registration with a username that is a reserved keyword
        self.fill_form(username="admin")
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Username 'admin' is reserved"), "Reserved username restriction not displayed.")

    def test_session_expiry_during_registration(self):
        # Test behavior when session expires during the registration process
        self.fill_form(username="testuser", email="testuser@example.com")
        self.simulate_session_expiry()
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Session expired. Please log in again."), "Session expiry message not displayed correctly.")
        self.assertTrue(self.check_data_persistence(), "Data not preserved after session expiry.")

    def solve_captcha(self):
        # Placeholder for CAPTCHA interaction
        pass

    def simulate_server_error(self):
        # Placeholder function to simulate a server error
        pass

    def simulate_high_traffic(self):
        # Placeholder function to simulate high traffic
        pass

    def simulate_session_expiry(self):
        # Placeholder function to simulate session expiry
        pass

    def check_data_persistence(self):
        # Verify that data persists after session expiry
        username_field = self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]')
        email_field = self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Email"]')
        return username_field.text == "testuser" and email_field.text == "testuser@example.com"

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
