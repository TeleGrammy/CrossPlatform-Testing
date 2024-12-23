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
from utils.scrolling import scroll_down_until_element_found, scroll_up_until_element_found
from utils.messaging import reply_to_message, edit_message, delete_message, forward_message
from utils.user import get_user_profile_info, get_user_privacy_settings, login_to_system, logout_from_system, user_add_story, update_user_profile_info, verify_user_signup, signup_to_system