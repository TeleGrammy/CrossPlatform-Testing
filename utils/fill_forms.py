from enums.xpaths import XPaths
from utils.scrolling import scroll_until_element_found
from selenium.webdriver.common.by import By

def clear_all_signup_fields(driver):
    # This function is used to clear all fields in registration form
    signup_form_xpath = [XPaths.USERNAME_FIELD, XPaths.EMAIL_FIELD, XPaths.PHONE_FIELD, XPaths.PASSWORD_FIELD,
                         XPaths.CONFIRM_PASSWORD_FIELD]
    for xpath in signup_form_xpath:
        scroll_until_element_found(driver, By.XPATH, xpath.value)
        driver.find_element_by_xpath(xpath.value).clear()
    driver.hide_keyboard()


def fill_signup_form(driver, username, email, phone, password, conf_password):
    # Fill form method to enter values into form fields
    clear_all_signup_fields(driver)
    driver.find_element_by_xpath(XPaths.USERNAME_FIELD.value).send_keys(username)
    driver.find_element_by_xpath(XPaths.EMAIL_FIELD.value).send_keys(email)
    driver.find_element_by_xpath(XPaths.PHONE_FIELD.value).send_keys(phone)
    driver.find_element_by_xpath(XPaths.PASSWORD_FIELD.value).send_keys(password)
    driver.find_element_by_xpath(XPaths.CONFIRM_PASSWORD_FIELD.value).send_keys(conf_password)
    driver.hide_keyboard()