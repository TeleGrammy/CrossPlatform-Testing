from selenium.webdriver import Keys

from enums.xpaths import XPaths
from utils.scrolling import scroll_down_until_element_found
from selenium.webdriver.common.by import By

def clear_all_signup_fields(driver):
    signup_form_xpath = [XPaths.USERNAME_FIELD, XPaths.EMAIL_FIELD, XPaths.PHONE_FIELD]
    driver.hide_keyboard() if driver.is_keyboard_shown() else None
    for xpath in signup_form_xpath:
        scroll_down_until_element_found(driver, By.XPATH, xpath.value, 5)
        driver.find_element(By.XPATH, xpath.value).click()
        driver.find_element( By.XPATH, xpath.value).clear()

    scroll_down_until_element_found(driver, By.XPATH, XPaths.PASSWORD_FIELD.value, 5)
    driver.find_element(By.XPATH, XPaths.PASSWORD_FIELD.value).click()
    driver.find_element(By.XPATH, XPaths.PASSWORD_ENTER_TEXT.value).clear()
    scroll_down_until_element_found(driver, By.XPATH, XPaths.CONFIRM_PASSWORD_ENTER_TEXT.value, 5)
    driver.find_element(By.XPATH, XPaths.CONFIRM_PASSWORD_ENTER_TEXT.value).click()
    driver.find_element(By.XPATH, XPaths.CONFIRM_PASSWORD_ENTER_TEXT.value).clear()

    driver.hide_keyboard()


def fill_signup_form(driver, username, email, phone, password, conf_password):
    clear_all_signup_fields(driver)
    driver.find_element(By.XPATH, XPaths.USERNAME_FIELD.value).click()
    driver.find_element( By.XPATH, XPaths.USERNAME_FIELD.value).send_keys(username)
    driver.find_element(By.XPATH, XPaths.EMAIL_FIELD.value).click()
    driver.find_element( By.XPATH, XPaths.EMAIL_FIELD.value).send_keys(email)
    driver.find_element(By.XPATH, XPaths.PHONE_FIELD.value).click()
    driver.find_element( By.XPATH, XPaths.PHONE_FIELD.value).send_keys(phone)
    driver.find_element( By.XPATH, XPaths.PASSWORD_FIELD.value).click()
    driver.find_element( By.XPATH, XPaths.PASSWORD_ENTER_TEXT.value).send_keys(password)
    scroll_down_until_element_found(driver, By.XPATH, XPaths.CONFIRM_PASSWORD_ENTER_TEXT.value, 5)
    driver.find_element( By.XPATH, XPaths.CONFIRM_PASSWORD_ENTER_TEXT.value).click()
    driver.find_element( By.XPATH, XPaths.CONFIRM_PASSWORD_ENTER_TEXT.value).send_keys(conf_password)
    driver.find_element(By.XPATH, XPaths.LOGO.value).click()
    driver.hide_keyboard()