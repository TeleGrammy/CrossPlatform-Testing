from appium import webdriver
import unittest

class DuplicateAccountPreventionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capabilities = {
            "platformName": 'Android',
            "deviceName": '146ce6c8',
            "app": r'C:\Users\20115\Downloads\app-release.apk'
        }
        cls.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', capabilities)
        cls.driver.implicitly_wait(50)

    def test_prevent_duplicate_email(self):
        # Test preventing duplicate accounts with the same email address
        self.register_user("duplicate_user", "duplicate@email.com", "Password123!")
        self.assertTrue(self.check_error_message("An account with this email already exists."), "Duplicate email account creation not prevented.")

    def test_prohibited_characters_in_username(self):
        # Test disallowing prohibited characters and spaces in usernames
        invalid_username = "invalid@user"
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]').send_keys(invalid_username)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertTrue(self.check_error_message("Invalid characters in username."), "Prohibited characters in username not handled properly.")

    def test_case_sensitivity_in_email(self):
        # Verify if email case sensitivity is correctly handled (e.g., user@email.com vs. User@email.com)
        self.register_user("testuser", "User@Email.com", "Password123!")
        duplicate_email_case = "user@email.com"
        self.register_user("testuser2", duplicate_email_case, "Password123!")
        self.assertTrue(self.check_error_message("An account with this email already exists."), "Duplicate emails with different cases treated as unique.")

    def test_long_username_handling(self):
        # Test handling of very long usernames within allowed input length
        long_username = "a" * 255  # Assuming the limit is 255 characters
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]').send_keys(long_username)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()
        self.assertFalse(self.check_error_message("Username is too long."), "Username length limit incorrectly enforced.")

    def test_duplicate_username_handling(self):
        # Verify prevention of duplicate usernames
        self.register_user("duplicateuser", "duplicate@example.com", "Password123!")
        self.register_user("duplicateuser", "unique@example.com", "Password123!")
        self.assertTrue(self.check_error_message("Username already in use."), "Duplicate usernames are not prevented.")

    def test_social_media_duplicate_account_prevention(self):
        # Check prevention of duplicate accounts for the same social media profile
        self.register_social_account("google", "uniqueuser@gmail.com")
        duplicate_social_email = "uniqueuser@gmail.com"
        self.register_social_account("google", duplicate_social_email)
        self.assertTrue(self.check_error_message("An account with this social profile already exists."), "Duplicate accounts for social media profiles not prevented.")

    def test_reregister_after_deactivation(self):
        # Test behavior for re-registering with the same email after deactivation
        self.deactivate_account("testuser@example.com")
        self.register_user("newuser", "testuser@example.com", "Password123!")
        self.assertTrue(self.check_successful_registration(), "Re-registration with a previously used email after deactivation failed.")

    def register_user(self, username, email, password):
        # Helper function to register a user
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]').send_keys(username)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Email"]').send_keys(email)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Password"]').send_keys(password)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()

    def register_social_account(self, platform, email):
        # Placeholder for registering with a social media account
        # Could include selecting a platform (e.g., Google) and entering the social account email
        pass

    def deactivate_account(self, email):
        # Placeholder to simulate deactivating an account
        # In real tests, this would involve API or UI steps to deactivate the account
        pass

    def check_error_message(self, expected_message):
        # Helper function to verify specific error messages
        error_element = self.driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Error Message']")
        return expected_message in error_element.text

    def check_successful_registration(self):
        # Placeholder method to verify successful registration
        success_element = self.driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Success Message']")
        return "Registration successful" in success_element.text

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
