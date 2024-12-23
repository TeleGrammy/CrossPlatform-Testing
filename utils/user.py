import time
import os
from selenium.webdriver.common.by import By
from utils.emails import EmailVerification
from enums.xpaths import XPaths
from utils.fill_forms import fill_signup_form
from utils.scrolling import scroll_down_until_element_found


def signup_to_system(driver, **user_credentials):
    username = user_credentials.get('username')
    email = user_credentials.get('email')
    phone = user_credentials.get('phone')
    password = user_credentials.get('password')
    confirm_password = user_credentials.get('confirm_password')

    fill_signup_form(driver, username, email, phone, password, confirm_password)
    driver.find_element(By.XPATH,XPaths.CAPATCHA_CHECK.value).click()
    time.sleep(3)
    driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).click()

def login_to_system(driver, email, password):
    scroll_down_until_element_found(driver, By.XPATH, XPaths.LOGIN_BUTTON_IN_REGISTER_FORM.value, 5)
    driver.find_element(By.XPATH,XPaths.LOGIN_BUTTON_IN_REGISTER_FORM.value).click()
    driver.find_element(By.XPATH, XPaths.LOGIN_FORM_EMAIL_ADDRESS_FIELD.value).click()
    driver.find_element(By.XPATH,XPaths.LOGIN_FORM_EMAIL_ADDRESS_FIELD.value).send_keys(email)
    driver.find_element(By.XPATH, XPaths.LOGIN_FORM_PASSWORD_FIELD.value).click()
    driver.find_element(By.XPATH,XPaths.LOGIN_FORM_PASSWORD_FIELD_SEND_KEYS.value).send_keys(password)
    driver.find_element(By.XPATH,XPaths.LOGIN_FORM_LOGIN_BUTTON.value).click()
    time.sleep(2)


def logout_from_system(driver):
    pass

def verify_user_signup(driver):
    time.sleep(2)
    if driver.find_element(By.XPATH,XPaths.SIGNUP_BUTTON.value).is_displayed():
        return 1
    code = EmailVerification.get_verification_code(
        os.getenv('EMAIL'),
        os.getenv('EMAIL_PASSWORD'),
        os.getenv('FROM')
    )
    time.sleep(5)
    if code is None:
        return code
    driver.find_element(By.XPATH,XPaths.SIGNUP_VERIFICATION_CODE_FIELD.value).send_keys(code)
    driver.find_element(By.XPATH,XPaths.SIGNUP_VERIFY_CONFIRMATION_CODE_BUTTON.value).click()
    driver.find_element(By.XPATH,XPaths.VERIFICATION_PAGE_BACK_BUTTON.value).click()
    return code

def get_user_profile_info(driver):
    driver.find_element(By.XPATH,XPaths.PROFILE_ICON.value).click()
    screen_name = driver.find_element(By.XPATH,XPaths.PROFILE_INFO_SCREEN_NAME_SHOWN.value).text
    username = driver.find_element(By.XPATH,XPaths.PROFILE_INFO_USERNAME.value).text
    email = driver.find_element(By.XPATH,XPaths.PROFILE_INFO_EMAIL.value).text
    phone = driver.find_element(By.XPATH,XPaths.PROFILE_INFO_PHONE.value).text
    profile_picture = ''
    scroll_down_until_element_found(driver, By.XPATH, XPaths.PROFILE_INFO_BIO.value, 5)
    bio = driver.find_element(By.XPATH,XPaths.PROFILE_INFO_BIO.value).text
    time.sleep(2)
    return {
        'screen_name': screen_name,
        'username': username,
        'email': email,
        'phone': phone,
        'profile_photo': profile_picture,
        'bio': bio
    }

def get_user_privacy_settings(driver):
    driver.find_element(By.XPATH,XPaths.PROFILE_ICON.value).click()
    scroll_down_until_element_found(driver, By.XPATH, XPaths.PROFILE_INFO_PRIVACY_SETTINGS.value, 5)
    driver.find_element(By.XPATH,XPaths.PROFILE_INFO_PRIVACY_SETTINGS.value).click()
    last_seen = driver.find_element(By.XPATH,XPaths.PRIVACY_SETTINGS_LAST_SEEN.value).text
    profile_photo_visibility = driver.find_element(By.XPATH,
        XPaths.PRIVACY_SETTINGS_PROFILE_PHOTO_VISIBILITY.value).text
    stories_visibility = driver.find_element(By.XPATH,XPaths.PRIVACY_SETTINGS_STORIES_VISIBILITY.value).text
    return {
        'last_seen': last_seen,
        'profile_photo_visibility': profile_photo_visibility,
        'stories_visibility': stories_visibility
    }

def user_add_story(driver, story_caption, camera_or_gallery):
    driver.find_element(By.XPATH,XPaths.PROFILE_ICON.value).click()
    scroll_down_until_element_found(driver, By.XPATH, XPaths.PROFILE_INFO_MY_STORIES.value, 5)
    driver.find_element(By.XPATH,XPaths.PROFILE_INFO_MY_STORIES.value).click()
    driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_BUTTON.value).click()
    if story_caption:
        driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_CAPTION.value).send_keys(story_caption)
    if camera_or_gallery == 1:
        driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_GALLERY_BUTTON.value).click()
        driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_GALLERY_PHOTO.value).click()
    elif camera_or_gallery == 2:
        driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_CAMERA_BUTTON.value).click()
        driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_CAMERA_TAKE_PHOTO_BUTTON.value).click()
    driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_PUBLISH_BUTTON.value).click()
    driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_OK_BUTTON.value).click()
    driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_BACK_BUTTON.value).click()

def update_user_profile_info(driver, new_info):
    driver.find_element(By.XPATH,XPaths.PROFILE_ICON.value).click()
    driver.find_element(By.XPATH,XPaths.PROFILE_INFO_EDIT_PROFILE_BUTTON.value).click()

    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_SCREEN_NAME_FIELD.value).send_keys(new_info['screen_name'])
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_BIO_FIELD.value).send_keys(new_info['bio'])
    driver.find_element(By.XPATH,XPaths.EDIT_CHANGE_PROFILE_PHOTO_BUTTON.value).click()
    driver.find_element(By.XPATH,XPaths.PROFILE_INFO_UPDATE_PHOTO.value).click()
    driver.find_element(By.XPATH,XPaths.STORIES_ADD_STORY_GALLERY_PHOTO.value).click()
    time.sleep(5)  # wait until upload is finished
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_SAVE_CHANGES_BUTTON.value).click()

    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_USERNAME.value).click()
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_USERNAME_FIELD.value).send_keys(new_info['username'])
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_USERNAME_SAVE_CHANGES_BUTTON.value).click()
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_USERNAME_BACK_BUTTON.value).click()

    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_EMAIL.value).click()
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_EMAIL_FIELD.value).send_keys(new_info['email'])
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_EMAIL_SAVE_CHANGES_BUTTON.value).click()
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_EMAIL_BACK_BUTTON.value).click()

    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_PHONE.value).click()
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_PHONE_FIELD.value).send_keys(new_info['phone_number'])
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_PHONE_SAVE_CHANGES_BUTTON.value).click()
    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_CHANGE_PHONE_BACK_BUTTON.value).click()

    driver.find_element(By.XPATH,XPaths.EDIT_PROFILE_BACK_BUTTON.value).click()