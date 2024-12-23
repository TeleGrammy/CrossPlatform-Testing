import os
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.user import get_user_profile_info, login_to_system, logout_from_system, update_user_profile_info

load_dotenv()

class ProfileInfoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)


    def test_user_info_persistence(self):
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")

        user_info_1 = get_user_profile_info(self.driver)
        logout_from_system(self.driver)
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")

        user_info_2 = get_user_profile_info(self.driver)
        self.assertTrue(user_info_1 != user_info_2, "User profile info persistence failed.")

    def test_user_changes_profile_info(self):
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")
        # new_info = self.get_user_new_info_for_update()
        new_info = {
            'screen_name': 'Mohamed Sayed',
            'username': 'mohamed23',
            'email': 'mo33sayed@gmail.com',
            'profile_photo': 'from gallery',
            'phone': '01150134573',
            'bio': 'this is my new bio'
        }
        update_user_profile_info(self.driver, new_info)

        logout_from_system(self.driver)

        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")

        user_info = get_user_profile_info(self.driver)
        check_user_info_is_updated = ProfileInfoTests.compare_user_info(user_info, new_info)
        self.assertTrue(check_user_info_is_updated, "User can not change profile info failed.")

    def get_user_new_info_for_update(self):
        pass

    @classmethod
    def compare_user_info(cls, user_info, new_info):
        return (
                user_info['email']==new_info['email'] and
                user_info['username']==new_info['username'] and
                user_info['phone']==new_info['phone'] and
                user_info['bio']==new_info['bio'] and
                user_info['screen_name']==new_info['screen_name'] and
                user_info['profile_photo']==new_info['profile_photo'])

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()