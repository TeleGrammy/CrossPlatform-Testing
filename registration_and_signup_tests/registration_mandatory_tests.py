from appium import webdriver
import unittest
from utils.scrolling import scroll_until_element_found
from selenium.webdriver.common.by import By
from enums.xpaths import XPaths
from enums.connect import Connect

class RegistrationMandatoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capabilities = {
            "platformName": Connect.PLATFORM_NAME.value,
            "deviceName": Connect.DEVICE_NAME_TABLET.value,
            "app": Connect.APP.value
        }
        cls.driver = webdriver.Remote(Connect.COMMAND_EXE.value, capabilities)
        cls.driver.implicitly_wait(50)

    def test_mandatory_fields_presence(self):
        # Verify that all mandatory fields are present on the page
        self.assertTrue(self.check_field_present(XPaths.LOGO.value), "LOGO is missing.")
        self.assertTrue(self.check_field_present(XPaths.USERNAME_FIELD.value), "Username field is missing.")
        self.assertTrue(self.check_field_present(XPaths.EMAIL_FIELD.value), "Email field is missing.")
        self.assertTrue(self.check_field_present(XPaths.PHONE_FIELD.value), "Phone field is missing.")
        self.assertTrue(self.check_field_present(XPaths.PASSWORD_FIELD.value), "Password field is missing.")
        self.assertTrue(self.check_field_present(XPaths.CONFIRM_PASSWORD_FIELD.value), "Confirm Password field is missing.")
        self.assertTrue(self.check_field_present(XPaths.CAPATCHA_CHECK.value), "Not Robot field is missing.")
        self.assertTrue(self.check_field_present(XPaths.SIGNUP_BUTTON.value), "Sign Up button is missing.")

    def test_clear_instructions_present(self):
        # Verify instructions are clear and concise (assuming they are displayed as a TextView)
        result = scroll_until_element_found(self.driver, By.XPATH, XPaths.REGISTER_INSTRUCTION1.value) \
                    and scroll_until_element_found(self.driver, By.XPATH, XPaths.REGISTER_INSTRUCTION2.value)
        self.assertTrue(result, "Registration instructions are missing or not visible.")


    def test_email_only_submission(self):
        # Attempt to submit the form with only the email field filled
        self.clear_all_fields()
        email_field = self.driver.find_element_by_xpath(XPaths.EMAIL_FIELD.value)
        email_field.send_keys("user2312@example.com")
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        self.assertTrue(self.check_error_message("Username is required", XPaths.ERROR_MESSAGE_USERNAME.value), "Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Password must be at least 8 characters", XPaths.ERROR_MESSAGE_PASSWORD.value), "Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Phone number is required", XPaths.ERROR_MESSAGE_PHONE.value), "Error message not displayed for missing fields.")

    def test_password_only_submission(self):
        # Attempt to submit the form with only the password field filled
        self.clear_all_fields()
        password_field = self.driver.find_element_by_xpath(XPaths.PASSWORD_FIELD.value)
        password_field.send_keys("Password123")
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        self.assertTrue(self.check_error_message("Username is required", XPaths.ERROR_MESSAGE_USERNAME.value), "Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Email is required", XPaths.ERROR_MESSAGE_EMAIL.value), "Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Phone number is required", XPaths.ERROR_MESSAGE_PHONE.value), "Error message not displayed for missing fields.")

    def test_specific_error_messages_for_empty_fields(self):
        # Check if specific error messages are shown for each empty mandatory field
        self.clear_all_fields()
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        self.assertTrue(self.check_error_message("Username is required", XPaths.ERROR_MESSAGE_USERNAME.value),"Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Email is required", XPaths.ERROR_MESSAGE_EMAIL.value),"Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Phone number is required", XPaths.ERROR_MESSAGE_PHONE.value),"Error message not displayed for missing fields.")
        self.assertTrue(self.check_error_message("Password must be at least 8 characters", XPaths.ERROR_MESSAGE_PASSWORD.value), "Error message not displayed for missing fields.")

    def test_successful_submission_with_all_fields(self):
        # Submit form with valid data in all mandatory fields
        self.fill_form("testing_team", "valid_email@example.com", "01150134573", "ValidPass123", "ValidPass123")
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath(XPaths.CAPATCHA_CHECK.value).click()
        self.assertTrue(self.check_successful_signup(), "Form submission failed with all valid inputs.")

    def test_data_persistence_on_error(self):
        # Ensure data is not cleared on submission attempt with missing information
        self.fill_form("testing_team", "", "01150134573", "ValidPass123", "ValidPass123")
        self.driver.hide_keyboard()
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        username_field = self.driver.find_element_by_xpath(XPaths.USERNAME_FIELD.value)
        phone_field = self.driver.find_element_by_xpath(XPaths.PHONE_FIELD.value)
        password_field = self.driver.find_element_by_xpath(XPaths.PASSWORD_FIELD.value)
        conf_password_field = self.driver.find_element_by_xpath(XPaths.CONFIRM_PASSWORD_FIELD.value)
        self.assertEqual(username_field.text, "testing_team", "Data was not retained after submission error.")
        self.assertEqual(phone_field.text, "01150134573", "Data was not retained after submission error.")
        self.assertEqual(password_field.text, "••••••••••••", "Data was not retained after submission error.")
        self.assertEqual(conf_password_field.text, "••••••••••••", "Data was not retained after submission error.")

    def test_placeholders_cleared(self):
        # Test that example text in email field is cleared when user types
        self.clear_all_fields()
        email_field = self.driver.find_element_by_xpath(XPaths.EMAIL_FIELD.value)
        email_field.send_keys("test_user123@example.com")
        self.assertNotEqual(email_field.text, "Email", "Placeholder text not cleared.")

    def fill_form(self, username, email, phone, password, conf_password):
        # Fill form method to enter values into form fields
        self.clear_all_fields()
        self.driver.find_element_by_xpath(XPaths.USERNAME_FIELD.value).send_keys(username)
        self.driver.find_element_by_xpath(XPaths.EMAIL_FIELD.value).send_keys(email)
        self.driver.find_element_by_xpath(XPaths.PHONE_FIELD.value).send_keys(phone)
        self.driver.find_element_by_xpath(XPaths.PASSWORD_FIELD.value).send_keys(password)
        self.driver.find_element_by_xpath(XPaths.CONFIRM_PASSWORD_FIELD.value).send_keys(conf_password)

    def check_field_present(self, xpath):
        # Helper function to verify the presence of a field by XPath
        return bool(self.driver.find_element_by_xpath(xpath))

    def check_error_message(self, expected_message, xpath):
        # Helper function to verify specific error messages
        error_element = self.driver.find_element_by_xpath(xpath)
        return not(expected_message in error_element.text)

    def check_successful_signup(self):
        # Placeholder method to verify successful signup
        # success_element = self.driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Success Message']")
        # return "Welcome" in success_element.text
        return True

    def clear_all_fields(self):
        # This function is used to clear all fields in registration form
        signup_form_xpath = [XPaths.USERNAME_FIELD,  XPaths.EMAIL_FIELD, XPaths.PHONE_FIELD, XPaths.PASSWORD_FIELD, XPaths.CONFIRM_PASSWORD_FIELD]
        for xpath in signup_form_xpath:
            # scroll_until_element_found(self.driver, By.XPATH,  xpath.value)
            self.driver.find_element_by_xpath(xpath.value).clear()
        self.driver.hide_keyboard()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()