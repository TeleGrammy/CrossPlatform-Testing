import os
import unittest
from appium import webdriver
from dotenv import load_dotenv
from enums.connect import Connect
from utils.user import login_to_system, user_add_story
from appium.options.android import UiAutomator2Options

load_dotenv()

class ScenarioThreeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_scenario_three(self):
        # Test login, then add a story, then change stories privacy settings, and upload another story
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))

        user_add_story(self.driver, story_caption='The first story', camera_or_gallery=1)
        # TODO: Verify successful upload a story
        # TODO: Verify the current story privacy settings is applied

        # TODO: Change stories privacy settings

        user_add_story(self.driver, story_caption='The second story', camera_or_gallery=1)
        # TODO: verify the story is uploaded and the caption is still same
        # TODO: Verify the new story privacy settings is applied



        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()