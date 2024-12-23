import os
import time
import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.fill_forms import fill_signup_form, clear_all_signup_fields
from utils.scrolling import scroll_down_until_element_found
from appium.options.android import UiAutomator2Options
from utils.user import signup_to_system, verify_user_signup, login_to_system

load_dotenv()

class RegistrationMandatoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_02_mandatory_fields_presence(self):
        self.assertTrue(self.check_field_present(XPaths.LOGO.value), "LOGO is missing.")
        self.assertTrue(self.check_field_present(XPaths.USERNAME_FIELD.value), "Username field is missing.")
        self.assertTrue(self.check_field_present(XPaths.EMAIL_FIELD.value), "Email field is missing.")
        self.assertTrue(self.check_field_present(XPaths.PHONE_FIELD.value), "Phone field is missing.")
        self.assertTrue(self.check_field_present(XPaths.PASSWORD_FIELD.value), "Password field is missing.")
        self.assertTrue(self.check_field_present(XPaths.CONFIRM_PASSWORD_FIELD.value), "Confirm Password field is missing.")
        self.assertTrue(self.check_field_present(XPaths.CAPATCHA_CHECK.value), "Not Robot field is missing.")
        self.assertTrue(self.check_field_present(XPaths.SIGNUP_BUTTON.value), "Sign Up button is missing.")

    def test_01_clear_instructions_present(self):
        result = scroll_down_until_element_found(self.driver, By.XPATH, XPaths.REGISTER_INSTRUCTION1.value) \
                 and scroll_down_until_element_found(self.driver, By.XPATH, XPaths.REGISTER_INSTRUCTION2.value)
        self.assertTrue(result, "Registration instructions are missing or not visible.")


    def test_05_email_only_submission(self):
        clear_all_signup_fields(self.driver)
        email_field = self.driver.find_element(By.XPATH,XPaths.EMAIL_FIELD.value)
        email_field.click()
        email_field.send_keys("user2312@example.com")
        time.sleep(1)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        self.assertTrue(self.check_error_message("Username is required", XPaths.ERROR_MESSAGE_USERNAME.value), "Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Password must be at least 8 characters", XPaths.ERROR_MESSAGE_PASSWORD.value), "Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Phone number is required", XPaths.ERROR_MESSAGE_PHONE.value), "Error message not displayed for missing fields.")

    def test_06_password_only_submission(self):
        clear_all_signup_fields(self.driver)
        password_field = self.driver.find_element(By.XPATH,XPaths.PASSWORD_FIELD.value)
        password_field.click()
        self.driver.find_element(By.XPATH,XPaths.PASSWORD_ENTER_TEXT.value).send_keys("Password123")
        self.driver.hide_keyboard()
        time.sleep(1)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        self.assertTrue(self.check_error_message("Username is required", XPaths.ERROR_MESSAGE_USERNAME.value), "Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Email is required", XPaths.ERROR_MESSAGE_EMAIL.value), "Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Phone number is required", XPaths.ERROR_MESSAGE_PHONE.value), "Error message not displayed for missing fields.")

    def test_07_specific_error_messages_for_empty_fields(self):
        clear_all_signup_fields(self.driver)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        self.assertTrue(self.check_error_message("Username is required", XPaths.ERROR_MESSAGE_USERNAME.value),"Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Email is required", XPaths.ERROR_MESSAGE_EMAIL.value),"Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Phone number is required", XPaths.ERROR_MESSAGE_PHONE.value),"Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Password must be at least 8 characters", XPaths.ERROR_MESSAGE_PASSWORD.value), "Error message not displayed for missing fields.")

    def test_08_successful_submission_with_all_fields(self):
        signup_to_system(self.driver,
                         username="test_user101",
                         email=os.getenv('EMAIL'),
                         phone="01150134555",
                         password="passtest123",
                         confirm_password="passtest123"
                         )

        code = verify_user_signup(self.driver)
        self.assertNotEqual(code, 1, "Nothing happened after click signup")
        self.assertTrue(code is not None, "Verification code was not sent")

        login_to_system(self.driver, os.getenv('EMAIL'), "testpass123")

        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")

    def test_03_data_persistence_on_error(self):
        fill_signup_form( self.driver,"testing_team", "", "01150134573", "ValidPass123", "ValidPass123")
        self.driver.hide_keyboard()
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        self.driver.find_element(By.XPATH, XPaths.USERNAME_FIELD.value).click()
        username_field = self.driver.find_element(By.XPATH,XPaths.USERNAME_FIELD.value).text
        self.driver.find_element(By.XPATH, XPaths.PHONE_FIELD.value).click()
        phone_field = self.driver.find_element(By.XPATH,XPaths.PHONE_FIELD.value).text
        self.driver.find_element(By.XPATH, XPaths.PASSWORD_FIELD.value).click()
        password_field = self.driver.find_element(By.XPATH,XPaths.PASSWORD_ENTER_TEXT.value).text
        self.driver.find_element(By.XPATH, XPaths.CONFIRM_PASSWORD_ENTER_TEXT.value).click()
        conf_password_field = self.driver.find_element(By.XPATH,XPaths.CONFIRM_PASSWORD_ENTER_TEXT.value).text
        self.assertEqual(username_field, "testing_team", "Data was not retained after submission error.")
        self.assertEqual(phone_field, "01150134573", "Data was not retained after submission error.")
        self.assertEqual(password_field, "••••••••••••", "Data was not retained after submission error.")
        self.assertEqual(conf_password_field, "••••••••••••", "Data was not retained after submission error.")

    def test_04_placeholders_cleared(self):
        clear_all_signup_fields(self.driver)
        email_field = self.driver.find_element(By.XPATH,XPaths.EMAIL_FIELD.value)
        email_field.send_keys("test_user123@example.com")
        self.assertNotEqual(email_field.text, "Email", "Placeholder text not cleared.")

    def check_field_present(self, xpath):
        return bool(self.driver.find_element(By.XPATH,xpath))

    def check_error_message(self, expected_message, xpath):
        error_element = self.driver.find_element(By.XPATH,xpath)
        return not(expected_message in error_element.text)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()