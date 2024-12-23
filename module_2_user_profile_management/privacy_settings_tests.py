import os
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from enums.connect import Connect
from utils.user import get_user_privacy_settings, login_to_system, logout_from_system

load_dotenv()

class PrivacySettingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)


    def test_user_privacy_settings_persistence(self):
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        user_privacy_settings1 = get_user_privacy_settings(self.driver)
        logout_from_system(self.driver)
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        user_privacy_settings2 = get_user_privacy_settings(self.driver)
        check_user_privacy_settings_persistence = PrivacySettingsTests.compare_user_privacy_settings(user_privacy_settings1, user_privacy_settings2)
        self.assertTrue(check_user_privacy_settings_persistence, "User privacy settings persistence test failed")

    def test_user_changes_privacy_settings(self):
       pass

    def test_user_blocked_contacts_persistence(self):
        pass

    def test_user_block_other_contacts(self):
        pass

    @classmethod
    def compare_user_privacy_settings(cls, settings1, settings2):
        return (
                settings1['last_seen']==settings2['last_seen'] and
                settings1['profile_photo_visibility']==settings2['profile_photo_visibility'] and
                settings1['stories_visibility']==settings2['stories_visibility'])
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()