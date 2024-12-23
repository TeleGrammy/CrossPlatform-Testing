import os
import unittest
from appium import webdriver
from dotenv import load_dotenv
from enums.connect import Connect
from utils.user import  login_to_system, user_add_story
from appium.options.android import UiAutomator2Options

load_dotenv()

class ScenarioFiveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_scenario_five(self):
        # Test user login then adds multiple stories then deletes them
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))

        stories_captions = ['first story', 'second story', 'third story']
        for story_caption in stories_captions:
            user_add_story(self.driver, story_caption=story_caption, camera_or_gallery=0)
            # TODO: verify the story is uploaded successfully

        # TODO: delete all stories
        # TODO: Verify all stories are deleted successfully

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()