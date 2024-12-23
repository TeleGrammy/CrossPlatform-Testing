import time
import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.fill_forms import fill_signup_form
from utils.user import  login_to_system, logout_from_system, user_add_story, verify_user_signup
from appium.options.android import UiAutomator2Options

load_dotenv()

class ScenarioSixTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_scenario_six(self):
        # Test user signup then login, then adds a story and change privacy settings
        # then deletes the story and adds another story, then logout, then login and open the stories

        fill_signup_form(self.driver, "test_user101", os.getenv('EMAIL'), "01150134555", "testpass123", "testpass123")
        self.driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()

        code = verify_user_signup(self.driver)
        self.assertNotEqual(code, 1, "Nothing happened after click signup")
        self.assertTrue(code is not None, "Verification code was not sent")

        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))

        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")

        user_add_story(self.driver, story_caption='My Story', camera_or_gallery=0)
        # TODO: verify the story is uploaded successfully

        # TODO: change user privacy settings
        # TODO: Verify that user privacy settings changed successfully

        # TODO: deletes the story
        # TODO: Verify the story is deleted

        user_add_story(self.driver, story_caption='My Second Story', camera_or_gallery=0)
        # TODO: verify the story is uploaded successfully

        logout_from_system(self.driver)

        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))

        # TODO: open stories and verify the story exists

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()