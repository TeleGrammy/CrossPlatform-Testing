import time

from appium import webdriver
import unittest
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.fill_forms import fill_signup_form
from utils.emails import EmailVerification
from dotenv import load_dotenv
import os

load_dotenv()

class DuplicateAccountPreventionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capabilities = {
            "platformName": Connect.PLATFORM_NAME.value,
            "deviceName": Connect.DEVICE_NAME_TABLET.value,
            "app": Connect.APP.value
        }
        cls.driver = webdriver.Remote(Connect.COMMAND_EXE.value, capabilities)
        cls.driver.implicitly_wait(50)

    def test_prevent_duplicate_email(self):
        # Test preventing duplicate accounts with the same email address
        fill_signup_form(self.driver, "test_user93", "visey22787@nozamas.com", "01150134544", "testpass123",
                         "testpass123")
        self.driver.find_element_by_xpath(XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        code = EmailVerification.get_verification_code(
            os.getenv('EMAIL'),
            os.getenv('EMAIL_PASSWORD'),
            os.getenv('FROM')
        )
        time.sleep(5)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_VERIFICATION_CODE_FIELD.value).send_keys(code)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_VERIFY_CONFIRMATION_CODE_BUTTON.value).click()
        try:
            self.driver.implicitly_wait(0)
            self.driver.find_element_by_xpath(XPaths.EXCEPTION_WHEN_SUBMIT_VERIFY_CODE.value)
        except Exception as e:
            self.assertTrue(True, "Exception occurred in verification code submission")
        finally:
            self.driver.implicitly_wait(50)
        # return to signup page and try to sign up with same email address
        time.sleep(5)
        fill_signup_form(self.driver, "test_user94", "visey22787@nozamas.com", "01150134533", "testpass143",
                         "testpass143")
        self.driver.find_element_by_xpath(XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        err_msg = self.driver.find_element_by_xpath(XPaths.ERROR_DUPLICATE_USERNAME.value)
        self.assertTrue(err_msg is not None, "Duplicate Phone numbers are not prevented.")


    def test_prevent_duplicate_phone(self):
        # Test prevent duplicate accounts with the same phone number
        fill_signup_form(self.driver, "test_user92", "visey22787@nozamas.com", "01150134544", "testpass123","testpass123")
        self.driver.find_element_by_xpath(XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        code = EmailVerification.get_verification_code(
            os.getenv('EMAIL'),
            os.getenv('EMAIL_PASSWORD'),
            os.getenv('FROM')
        )
        time.sleep(5)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_VERIFICATION_CODE_FIELD.value).send_keys(code)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_VERIFY_CONFIRMATION_CODE_BUTTON.value).click()
        try:
            self.driver.implicitly_wait(0)
            self.driver.find_element_by_xpath(XPaths.EXCEPTION_WHEN_SUBMIT_VERIFY_CODE.value)
        except Exception as e:
            self.assertTrue(True, "Exception occurred in verification code submission")
        finally:
            self.driver.implicitly_wait(50)
        # return to signup page and try to sign up with same phone number
        time.sleep(5)
        fill_signup_form(self.driver, "test_user91", "abdallahsalah55@gmail.com", "01150134544", "testpass143","testpass143")
        self.driver.find_element_by_xpath(XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        err_msg = self.driver.find_element_by_xpath(XPaths.ERROR_DUPLICATE_USERNAME.value)
        self.assertTrue(err_msg is not None, "Duplicate Phone numbers are not prevented.")

    def test_duplicate_username_handling(self):
        # Verify prevention of duplicate usernames
        fill_signup_form(self.driver, "test_user90", "visey22787@nozamas.com", "01150134544", "testpass123","testpass123")
        self.driver.find_element_by_xpath(XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(2)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        code = EmailVerification.get_verification_code(
            os.getenv('EMAIL'),
            os.getenv('EMAIL_PASSWORD'),
            os.getenv('FROM')
        )
        time.sleep(5)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_VERIFICATION_CODE_FIELD.value).send_keys(code)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_VERIFY_CONFIRMATION_CODE_BUTTON.value).click()
        try:
            self.driver.implicitly_wait(0)
            self.driver.find_element_by_xpath(XPaths.EXCEPTION_WHEN_SUBMIT_VERIFY_CODE.value)
        except Exception as e:
            self.assertTrue(True, "Exception occurred in verification code submission")
        finally:
            self.driver.implicitly_wait(50)
        # return to signup page and try to sign up with same username
        time.sleep(5)
        fill_signup_form(self.driver, "test_user90", "abdallahsalah55@gmail.com", "01556895454", "testpass123","testpass123")
        self.driver.find_element_by_xpath(XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(3)
        self.driver.find_element_by_xpath(XPaths.SIGNUP_BUTTON.value).click()
        err_msg = self.driver.find_element_by_xpath(XPaths.ERROR_DUPLICATE_USERNAME.value)
        self.assertTrue(err_msg is not None, "Duplicate usernames are not prevented.")

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
