import time
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.fill_forms import fill_signup_form
from appium.options.android import UiAutomator2Options



class RegistrationFieldValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_empty_individual_fields(self):
        # Test submission with each field empty one by one
        field_names = ["Username", "Email", "Phone", "Password", "Confirm Password"]
        error_msgs_xpath = [XPaths.ERROR_MESSAGE_USERNAME, XPaths.ERROR_MESSAGE_EMAIL, XPaths.ERROR_MESSAGE_PHONE, XPaths.ERROR_MESSAGE_PASSWORD, XPaths.ERROR_MESSAGE_CONFIRM_PASSWORD]
        fields_xpath = [XPaths.USERNAME_FIELD, XPaths.EMAIL_FIELD, XPaths.PHONE_FIELD, XPaths.PASSWORD_FIELD, XPaths.CONFIRM_PASSWORD_FIELD]
        for i in range(0, len(fields_xpath)-1):
            fill_signup_form(self.driver, "test_user456", "test_email@gmail.com", "01150134573", "testpass123", "testpass123")
            field_element = self.driver.find_element(By.XPATH,fields_xpath[i].value)
            field_element.clear()
            self.driver.hide_keyboard()
            self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
            err_msg = self.driver.find_element(By.XPATH, error_msgs_xpath[i].value)
            self.assertTrue( err_msg is not None, f"Error message for empty {field_names[i]} not displayed.")


    def test_invalid_email_format(self):
        # Test invalid email formats
        invalid_emails = ["user@", "user@domain", "user@domain@domain.com", "user@@domain.com"]
        fill_signup_form(self.driver, "test_user456", "", "01150134573", "testpass123", "testpass123")
        for email in invalid_emails:
            self.driver.find_element(By.XPATH,XPaths.EMAIL_FIELD.value).clear()
            self.driver.find_element(By.XPATH,XPaths.EMAIL_FIELD.value).send_keys(email)
            self.driver.hide_keyboard()
            self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
            email_err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_MESSAGE_INVALID_EMAIL.value)
            self.assertTrue(email_err_msg is not None, f"Invalid email '{email}' not detected.")

    def test_password_strength(self):
        # Test password strength requirements
        weak_passwords = ["short", "123", "pass", "12334567"]
        fill_signup_form(self.driver, "test_user456", "valid_test56@gmail.com", "01150134573", "", "")
        for password in weak_passwords:
            self.driver.find_element(By.XPATH,XPaths.PASSWORD_FIELD.value).send_keys(password)
            self.driver.find_element(By.XPATH,XPaths.CONFIRM_PASSWORD_FIELD.value).send_keys(password)
            self.driver.hide_keyboard()
            self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
            password_err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_MESSAGE_PASSWORD.value)
            self.assertTrue(password_err_msg is not None, f"Weak password '{password}' was not flagged.")

    def test_password_confirmation_match(self):
        # Test that password and confirmation must match
        fill_signup_form(self.driver, "test_user456", "valid_test78@gmail.com", "01150134573", "tstpass123", "tstpass133")
        self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        password_err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_PASSWORD_DO_NOT_MATCH.value)
        self.assertTrue(password_err_msg is not None, "Mismatched passwords not flagged.")

    def test_password_no_alphanumeric(self):
        # Test passwords with no alphanumeric characters
        non_alphanumeric_password = "*********"
        fill_signup_form(self.driver, "test_user456", "valid_test90@gmail.com", "01150134573", non_alphanumeric_password, non_alphanumeric_password)
        self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        password_err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_MESSAGE_PASSWORD.value)
        self.assertTrue(password_err_msg is not None, "Password with no alphanumeric characters not flagged.")

    def test_password_with_spaces_characters(self):
        # Test passwords containing spaces characters
        special_char_password = "Pass word!@#"
        fill_signup_form(self.driver, "test_user456", "valid_test21@gmail.com", "01150134573", special_char_password, special_char_password)
        self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        password_err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_MESSAGE_PASSWORD.value)
        self.assertTrue(password_err_msg is not None, "Password with spaces characters not accepted.")

    def test_common_passwords(self):
        # Test that commonly used passwords are not allowed
        common_passwords = ["password", "123456", "admin"]
        fill_signup_form(self.driver, "test_user456", "valid_test56@gmail.com", "01150134573", "", "")
        for password in common_passwords:
            self.driver.find_element(By.XPATH,XPaths.PASSWORD_FIELD.value).send_keys(password)
            self.driver.find_element(By.XPATH,XPaths.CONFIRM_PASSWORD_FIELD.value).send_keys(password)
            self.driver.hide_keyboard()
            self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
            password_err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_MESSAGE_PASSWORD.value)
            self.assertTrue(password_err_msg is not None, f"Common password '{password}' not flagged.")

    def test_invalid_username(self):
        # Test invalid usernames are not allowed
        invalid_usernames = ["a", "ab", "123123", "4"]
        fill_signup_form(self.driver, "", "valid_test43@gmail.com", "01150134573", "passTest123", "passTest123")
        for username in invalid_usernames:
            self.driver.find_element(By.XPATH,XPaths.USERNAME_FIELD.value).send_keys(username)
            self.driver.hide_keyboard()
            self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
            username_err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_MESSAGE_USERNAME.value)
            self.assertTrue(username_err_msg is not None, f"Invalid Username '{username}' not flagged.")

    def test_invalid_phone(self):
        # Test invalid phone are not allowed
        invalid_phones = ["0115013", "00000000000", "01434789234", "123123", "4"]
        fill_signup_form(self.driver, "test_user_123", "valid_test65@gmail.com", "", "passTest123", "passTest123")
        for phone in invalid_phones:
            self.driver.find_element(By.XPATH,XPaths.PHONE_FIELD.value).send_keys(phone)
            self.driver.hide_keyboard()
            self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
            phone_err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_MESSAGE_PHONE.value)
            self.assertTrue(phone_err_msg is not None, f"Invalid Phone Number '{phone}' not flagged.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
