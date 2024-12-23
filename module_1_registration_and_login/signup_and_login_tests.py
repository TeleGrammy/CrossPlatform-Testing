import time
import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.scrolling import scroll_down_until_element_found, scroll_up_until_element_found
from utils.user import login_to_system,  verify_user_signup, signup_to_system
from appium.options.android import UiAutomator2Options

load_dotenv()

class SignupAndLoginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_valid_signup_valid_login(self):
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
        # TODO: Verify the successful signup

        login_to_system(self.driver, os.getenv('EMAIL'), "passtest123")

        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")

    def test_valid_signup_invalid_login(self):
        signup_to_system(self.driver,
                         username="test_user102",
                         email=os.getenv('EMAIL'),
                         phone="01150134666",
                         password="testpass444",
                         confirm_password="testpass444"
                         )

        code = verify_user_signup(self.driver)
        self.assertNotEqual(code, 1, "Nothing happened after click signup")
        self.assertTrue(code is not None, "Verification code was not sent")

        login_to_system(self.driver, os.getenv('EMAIL'), "testpass123")

        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is None, "logged in to the system, while expected to fail")

        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_EMAIL_ADDRESS_FIELD.value).clear()
        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_PASSWORD_FIELD.value).clear()
        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_EMAIL_ADDRESS_FIELD.value).send_keys("test1user@gmail.com") #Wrong Email
        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_PASSWORD_FIELD.value).send_keys("testpass444")
        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_LOGIN_BUTTON.value).click()
        time.sleep(2)
        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is None, "logged in to the system, while expected to fail")

    def test_invalid_signup_try_login(self):
        signup_to_system(self.driver,
                         username="test_user101",
                         email="temp_email11@gmail.com",
                         phone="01150134555",
                         password="testpass000",
                         confirm_password="testpass000"
                         )
        # TODO: Verify the UN-successful signup

        self.driver.find_element(By.XPATH,XPaths.VERIFICATION_PAGE_BACK_BUTTON.value).click()
        scroll_down_until_element_found(self.driver, By.XPATH, XPaths.LOGIN_BUTTON_IN_REGISTER_FORM.value, 5)
        self.driver.find_element(By.XPATH,XPaths.LOGIN_BUTTON_IN_REGISTER_FORM.value).click()

        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_EMAIL_ADDRESS_FIELD.value).send_keys("temp_email11@gmail.com")
        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_PASSWORD_FIELD.value).send_keys("testpass000")
        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_LOGIN_BUTTON.value).click()
        time.sleep(2)
        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is None, "logged in to the system, while expected to fail")

    def test_invalid_signup_with_wrong_verification_then_login(self):
        # verify that signup is failed if user did not verify with code by try to login
        signup_to_system(self.driver,
                         username="test_user106",
                         email=os.getenv('EMAIL'),
                         phone="01150134999",
                         password="testpass121",
                         confirm_password="testpass121"
                         )
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_VERIFICATION_CODE_FIELD.value).send_keys("123456")
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_VERIFY_CONFIRMATION_CODE_BUTTON.value).click()
        # TODO: Verify the UN-successful signup

        self.driver.find_element(By.XPATH,XPaths.VERIFICATION_PAGE_BACK_BUTTON.value).click()

        login_to_system(self.driver, os.getenv('EMAIL'),"testpass121")

        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is None, "logged in to the system, while expected to fail")

    def test_invalid_signup_without_verification_then_login(self):
        # verify that signup is failed if user did not verify with code by try to login
        signup_to_system(self.driver,
                         username="test_user106",
                         email="test123testuser@gmail.com",
                         phone="01150134999",
                         password="testpass121",
                         confirm_password="testpass121"
                         )
        # TODO: Verify the UN-successful signup

        # Skip verification step
        self.driver.find_element(By.XPATH,XPaths.VERIFICATION_PAGE_BACK_BUTTON.value).click()

        login_to_system(self.driver, "test123testuser@gmail.com", "testpass121")

        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is None, "logged in to the system, while expected to fail")

    def test_forget_password(self):
        login_to_system(self.driver, os.getenv('EMAIL'), "wrongpassword")

        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is None, "logged in to the system, while expected to fail")

        new_password = "mynewpassword123"
        self.driver.find_element(By.XPATH,XPaths.LOGIN_FORM_FORGOT_PASSWORD_BUTTON.value).click()
        self.driver.find_element(By.XPATH,XPaths.FORGOT_PASSWORD_EMAIL_FIELD.value).send_keys(os.getenv('EMAIL'))
        self.driver.find_element(By.XPATH,XPaths.FORGOT_PASSWORD_CONTINUE_BUTTON.value).click()
        forgot_password_page = self.driver.find_element(By.XPATH, XPaths.FORGOT_PASSWORD_PAGE.value)
        self.assertTrue(forgot_password_page is not None, "Failed to update password")
        # TODO: continue updating password
        login_to_system(self.driver, os.getenv('EMAIL'), new_password)
        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()