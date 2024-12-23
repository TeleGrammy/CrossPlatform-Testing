import time
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.fill_forms import fill_signup_form
from utils.user import verify_user_signup, signup_to_system
from appium.options.android import UiAutomator2Options

load_dotenv()

class DuplicateAccountPreventionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_prevent_duplicate_email(self):
        # Test preventing duplicate accounts with the same email address
        signup_to_system(self.driver,
                         username="test_user93",
                         email="visey22787@nozamas.com",
                         phone="01150134544",
                         password="testpass123",
                         confirm_password="testpass123"
                         )

        code = verify_user_signup(self.driver)
        self.assertNotEqual(code, 1, "Nothing happened after click signup")
        self.assertTrue(code is not None, "Verification code was not sent")

        try:
            self.driver.implicitly_wait(0)
            self.driver.find_element(By.XPATH,XPaths.EXCEPTION_WHEN_SUBMIT_VERIFY_CODE.value)
        except Exception as e:
            self.assertTrue(True, "Exception occurred in verification code submission")
        finally:
            self.driver.implicitly_wait(50)
        # return to signup page and try to sign up with same email address
        time.sleep(5)
        fill_signup_form(self.driver, "test_user94", "visey22787@nozamas.com", "01150134533", "testpass143",
                         "testpass143")
        self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_DUPLICATE_USERNAME.value)
        self.assertTrue(err_msg is not None, "Duplicate Phone numbers are not prevented.")


    def test_prevent_duplicate_phone(self):
        # Test prevent duplicate accounts with the same phone number
        signup_to_system(self.driver,
                         username="test_user92",
                         email="visey22787@nozamas.com",
                         phone="01150134544",
                         password="testpass123",
                         confirm_password="testpass123"
                         )

        code = verify_user_signup(self.driver)
        self.assertNotEqual(code, 1, "Nothing happened after click signup")
        self.assertTrue(code is not None, "Verification code was not sent")

        try:
            self.driver.implicitly_wait(0)
            self.driver.find_element(By.XPATH,XPaths.EXCEPTION_WHEN_SUBMIT_VERIFY_CODE.value)
        except Exception as e:
            self.assertTrue(True, "Exception occurred in verification code submission")
        finally:
            self.driver.implicitly_wait(50)
        # return to signup page and try to sign up with same phone number
        time.sleep(5)
        fill_signup_form(self.driver, "test_user91", "abdallahsalah55@gmail.com", "01150134544", "testpass143","testpass143")
        self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_DUPLICATE_USERNAME.value)
        self.assertTrue(err_msg is not None, "Duplicate Phone numbers are not prevented.")

    def test_duplicate_username_handling(self):
        # Verify prevention of duplicate usernames
        signup_to_system(self.driver,
                         username="test_user90",
                         email="visey22787@nozamas.com",
                         phone="01150134544",
                         password="testpass123",
                         confirm_password="testpass123"
                         )

        code = verify_user_signup(self.driver)
        self.assertNotEqual(code, 1, "Nothing happened after click signup")
        self.assertTrue(code is not None, "Verification code was not sent")

        try:
            self.driver.implicitly_wait(0)
            self.driver.find_element(By.XPATH,XPaths.EXCEPTION_WHEN_SUBMIT_VERIFY_CODE.value)
        except Exception as e:
            self.assertTrue(True, "Exception occurred in verification code submission")
        finally:
            self.driver.implicitly_wait(50)
        # return to signup page and try to sign up with same username
        time.sleep(5)
        fill_signup_form(self.driver, "test_user90", "abdallahsalah55@gmail.com", "01556895454", "testpass123","testpass123")
        self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        err_msg = self.driver.find_element(By.XPATH,XPaths.ERROR_DUPLICATE_USERNAME.value)
        self.assertTrue(err_msg is not None, "Duplicate usernames are not prevented.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
