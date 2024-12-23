import time
import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from enums.connect import Connect
from utils.emails import EmailVerification
from enums.xpaths import XPaths
from utils.fill_forms import fill_signup_form
from appium.options.android import UiAutomator2Options

load_dotenv()

class EmailVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def register_and_trigger_email(self):
        fill_signup_form(self.driver, "tst262", os.getenv('EMAIL'), "01150134570", "passEasy123", "passEasy123")
        self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(3)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()
        time.sleep(5)
        return self.check_email_sent()

    def check_email_sent(self):
        # Placeholder function to check if verification email was sent
        try:
            code = EmailVerification.get_verification_code(
                os.getenv('EMAIL'),
                os.getenv('EMAIL_PASSWORD'),
                os.getenv('FROM')
            )
            return code
        except Exception as e:
            return None

    def test_verification_email_sent(self):
        # Verify that a verification email is sent upon successful registration
        email_sent = self.register_and_trigger_email()
        self.assertTrue(email_sent is not None, "Verification email was not sent.")

    def test_resend_verification_email(self):
        # Test the ability to resend a verification email if needed
        email1_code = self.register_and_trigger_email()
        self.assertTrue(email1_code is not None, "Verification email 1 was not sent.")
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_VERIFICATION_CODE_SEND_AGAIN.value).click()
        email2_code = self.check_email_sent()
        self.assertTrue(email2_code is not None, "Verification email 2 was not sent after click resend again.")
        self.assertTrue(email1_code != email2_code, "Resend verification email did not work as expected.")


    def test_multiple_clicks_on_verification_button(self):
        # Test multiple clicks on the verification link and verify there are no bad effects
        self.register_and_trigger_email()
        for _ in range(3):
            self.driver.find_element(By.XPATH,XPaths.SIGNUP_VERIFY_CONFIRMATION_CODE_BUTTON.value).click()
        err_msg = self.driver.find_element(By.XPATH,XPaths.EXCEPTION_WHEN_SUBMIT_VERIFY_CODE.value)
        self.assertTrue(err_msg is not None, "Multiple clicks on Verify button does not shown any message.")

    def test_verification_with_wrong_code(self):
        # Ensure attempting to verify an email with wrong verification code
        self.register_and_trigger_email()
        time.sleep(3)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_VERIFICATION_CODE_FIELD.value).send_keys("123456")
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_VERIFY_CONFIRMATION_CODE_BUTTON.value).click()
        err_msg = self.driver.find_element(By.XPATH,XPaths.EXCEPTION_WHEN_SUBMIT_VERIFY_CODE.value)
        self.assertTrue(err_msg is not None, "Wrong Verification code submission is not prevented.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
