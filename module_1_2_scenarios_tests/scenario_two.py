import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.user import login_to_system
from appium.options.android import UiAutomator2Options

load_dotenv()

class ScenarioTwoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_scenario_two(self):
        # Test failed login, then forget password, login, change privacy settings, delete a story
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

        # TODO: change user privacy settings
        # TODO: Verify that user privacy settings changed successfully

        # TODO: delete a story
        # TODO: Verify the story is deleted successfully


        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()