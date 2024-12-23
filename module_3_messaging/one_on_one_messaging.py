import time
import os
import unittest
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from enums.connect import Connect
from enums.xpaths import XPaths
from utils.scrolling import scroll_down_until_element_found, scroll_up_until_element_found
from utils.messaging import reply_to_message, edit_message, delete_message, forward_message
from utils.user import login_to_system


load_dotenv()

class OneOnOneMessaging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options().load_capabilities({
            'platformName': Connect.PLATFORM_NAME.value,
            'deviceName': Connect.EMULATOR_NAME.value,
            'app': Connect.APP.value,
        })
        cls.driver = webdriver.Remote(command_executor=Connect.COMMAND_EXE.value, options=options)
        cls.driver.implicitly_wait(50)

    def test_01_send_receive_messages(self):
        # test sending messages like text, audio, (emojis, stickers, gifs), reply messages
        # TODO: Verify sending and receiving messages is working as expected
        pass

    def test_02_edit_message(self):
        self.login_and_open_chat()
        # Try to edit me message
        updated_msg = 'Edited message'
        curr_msg = edit_message(self.driver,  XPaths.MESSAGING_ME_MESSAGE_11.value, updated_msg)
        self.assertTrue(updated_msg == curr_msg, "Me message was not edited, while expecting to")

        # Try to edit other user message
        curr_msg = edit_message(self.driver, XPaths.MESSAGING_OTHER_MESSAGE_1.value, updated_msg)
        self.assertTrue(updated_msg != curr_msg, "Other user message was edited, while expecting not")

    def test_03_delete_message(self):
        self.driver.terminate_app('com.example.telegrammy')
        time.sleep(2)
        self.driver.activate_app('com.example.telegrammy')
        self.login_and_open_chat()

        # Try to delete me message
        scroll_up_until_element_found(self.driver, By.XPATH, XPaths.MESSAGING_ME_MESSAGE_1.value, 5)
        delete_message(self.driver,  XPaths.MESSAGING_ME_MESSAGE_1.value)
        check = scroll_up_until_element_found(self.driver, By.XPATH, XPaths.MESSAGING_ME_MESSAGE_1.value, 5)
        self.assertTrue(not check, "Deleting a me message failed.")

        # Try to delete other user message
        scroll_up_until_element_found(self.driver, By.XPATH, XPaths.MESSAGING_OTHER_MESSAGE_1.value, 5)
        delete_message(self.driver,  XPaths.MESSAGING_OTHER_MESSAGE_1.value)
        check = scroll_up_until_element_found(self.driver, By.XPATH, XPaths.MESSAGING_OTHER_MESSAGE_1.value, 5)
        self.assertTrue(check, "Deleting other user message done, while expecting to fail.")

    def test_04_reply_to_message(self):
        self.driver.terminate_app('com.example.telegrammy')
        time.sleep(2)
        self.driver.activate_app('com.example.telegrammy')
        self.login_and_open_chat()

        # Try to reply to me message
        reply_msg = 'This is a reply message'
        scroll_up_until_element_found(self.driver, By.XPATH, XPaths.MESSAGING_ME_MESSAGE_2.value, 5)
        reply_to_message(self.driver, XPaths.MESSAGING_ME_MESSAGE_1.value, reply_msg)
        check = scroll_down_until_element_found(self.driver, By.XPATH, XPaths.MESSAGING_REPLY_TO_ME_MESSAGE_2.value, 5)
        self.assertTrue(check, "Reply to me message failed.")

        # Try to reply to other user message
        scroll_up_until_element_found(self.driver, By.XPATH, XPaths.MESSAGING_OTHER_MESSAGE_2.value, 5)
        reply_to_message(self.driver, XPaths.MESSAGING_OTHER_MESSAGE_1.value, reply_msg)
        check = scroll_down_until_element_found(self.driver, By.XPATH, XPaths.MESSAGING_REPLY_TO_OTHER_MESSAGE_2.value,5)
        self.assertTrue(check, "Reply to other message failed.")

    def test_05_forward_message(self):
        self.driver.terminate_app('com.example.telegrammy')
        time.sleep(2)
        self.driver.activate_app('com.example.telegrammy')
        self.login_and_open_chat()

        # try forward me message
        forward_message(self.driver, XPaths.MESSAGING_ME_MESSAGE_1, XPaths.MESSAGING_FORWARD_TO_ALICE_MOCK)
        time.sleep(1)
        element = self.driver.find_element(By.XPATH, XPaths.MESSAGING_CHAT_BACK_BUTTON.value)
        self.assertTrue(element.is_displayed(), "Application crashes during forward message attempt")

        # TODO: Verify that the message is sent to the target user

        # try forward other message
        forward_message(self.driver, XPaths.MESSAGING_OTHER_MESSAGE_1, XPaths.MESSAGING_FORWARD_TO_ALICE_MOCK)
        time.sleep(1)
        element = self.driver.find_element(By.XPATH, XPaths.MESSAGING_CHAT_BACK_BUTTON.value)
        self.assertTrue(element.is_displayed(), "Application crashes during forward message attempt")

        # TODO: Verify that the message is sent to the target user


        # TODO: Try to use search in forward message page
        # TODO: Verify that search in forward message is working fine


    def test_06_mute_notifications(self):
        self.driver.terminate_app('com.example.telegrammy')
        time.sleep(2)
        self.driver.activate_app('com.example.telegrammy')
        self.login_and_open_chat()

        self.driver.find_element(By.XPATH,XPaths.MESSAGING_OPTIONS_ICON.value).click()
        self.driver.find_element(By.XPATH,XPaths.MESSAGING_OPTIONS_MUTE.value).click()
        self.driver.find_element(By.XPATH,XPaths.MESSAGING_OPTIONS_MUTE_ONE_HOUR.value).click()

        element = self.driver.find_element(By.XPATH, XPaths.MESSAGING_OPTIONS_MUTE_ONE_HOUR.value)
        self.assertTrue(not element.is_displayed(), "Application does not respond after clicking mute.")


        # TODO: Verify this chat will be mute for one hour

        self.driver.find_element(By.XPATH,XPaths.MESSAGING_OPTIONS_ICON.value).click()
        self.driver.find_element(By.XPATH,XPaths.MESSAGING_OPTIONS_MUTE.value).click()
        self.driver.find_element(By.XPATH, XPaths.MESSAGING_OPTIONS_MUTE_PERMANENT.value).click()

        element = self.driver.find_element(By.XPATH, XPaths.MESSAGING_OPTIONS_MUTE_PERMANENT.value)
        self.assertTrue(not element.is_displayed(), "Application does not respond after clicking mute.")

        # TODO: Verify this chat will be mute permanent


    def test_07_mention_other_users(self):
        # TODO: test the functionality of mentioning other users in a chat
        pass


    def login_and_open_chat(self):
        login_to_system(self.driver, os.getenv('EMAIL'), os.getenv('ACCOUNT_PASSWORD'))
        profile_icon = self.driver.find_element(By.XPATH, XPaths.PROFILE_ICON.value)
        self.assertTrue(profile_icon is not None, "Failed to login to the system")
        self.driver.tap([(400, 280)], 2000)
        allow_rcd_audio = self.driver.find_element(By.XPATH, XPaths.MESSAGING_ALLOW_RECORD_AUDIO.value)
        allow_rcd_audio.click() if allow_rcd_audio.is_displayed() else None

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()