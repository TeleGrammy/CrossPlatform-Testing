import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.user import get_user_profile_info, login_to_system, logout_from_system, user_add_story, update_user_profile_info, verify_user_signup, signup_to_system
from appium.options.android import UiAutomator2Options


load_dotenv()

class ScenarioOneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_scenario_one(self):
        # Test signup, verification email, login, add a story, change profile info, then change privacy settings
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

        login_to_system(self.driver,os.getenv('EMAIL'), "testpass123")

        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")

        user_add_story(self.driver, story_caption="Scenario one story", camera_or_gallery=1)
        # TODO: Verify successful upload a story


        # new_info = self.get_user_new_info_for_update()
        new_info = {
            'screen_name': 'Mohamed Sayed',
            'username': 'mohamed23',
            'email': 'mo33sayed@gmail.com',
            'profile_photo': 'from gallery',
            'phone_number': '01150134573',
            'bio': 'this is my new bio'
        }
        update_user_profile_info(self.driver, new_info)

        logout_from_system(self.driver)

        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))

        user_info = get_user_profile_info(self.driver)
        check_user_info_is_updated = ScenarioOneTest.compare_user_info(user_info, new_info)
        self.assertTrue(check_user_info_is_updated, "User can not change profile info: failed.")

        # TODO: change user privacy settings
        # TODO: Verify that user privacy settings changed successfully


    def get_user_new_info_for_update(self):
        pass

    @classmethod
    def compare_user_info(cls, user_info, new_info):
        return (
                user_info['email']==new_info['email'] and
                user_info['username']==new_info['username'] and
                user_info['phone']==new_info['phone_number'] and
                user_info['bio']==new_info['bio'] and
                user_info['screen_name']==new_info['screen_name'] and
                user_info['profile_picture']==new_info['profile_photo'] and
                user_info['phone_number']==new_info['phone_number'])
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()