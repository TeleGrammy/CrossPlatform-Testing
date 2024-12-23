import os
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from enums.connect import Connect
from utils.user import login_to_system, user_add_story

load_dotenv()

class StoriesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_user_add_story_with_text_only(self):
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        user_add_story(self.driver, story_caption='hello world', camera_or_gallery=0)

        # TODO: verify the story is uploaded successfully


    def test_user_add_story_with_photo_only(self):
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        user_add_story(self.driver, story_caption=None, camera_or_gallery=1)

        # TODO: verify the story is uploaded successfully

    def test_user_add_story_with_text_and_gallery_photo(self):
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        user_add_story(self.driver, story_caption='This is a test caption', camera_or_gallery=1)

        # TODO: verify the story is uploaded successfully

    def test_user_add_story_with_text_and_camera_photo(self):
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        user_add_story(self.driver, story_caption='This is a test caption', camera_or_gallery=2)

        # TODO: verify the story is uploaded successfully

    def test_user_change_stories_settings(self):
        pass
    def test_user_delete_story(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()