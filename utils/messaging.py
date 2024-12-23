from enums.xpaths import XPaths
from selenium.webdriver.common.by import By

def edit_message(driver, msg_element, new_msg):
    msg = driver.find_element(By.ID,msg_element)
    driver.long_press(msg, duration=1000).release().perform()
    driver.find_element(By.XPATH,XPaths.MESSAGING_MESSAGE_HOLD_OPTS_EDIT.value).click()
    driver.find_element(By.XPATH,XPaths.MESSAGING_MESSAGE_FIELD.value).clear()
    driver.find_element(By.XPATH,XPaths.MESSAGING_MESSAGE_FIELD.value).send_keys(new_msg)
    driver.find_element(By.XPATH,XPaths.MESSAGING_SEND_MESSAGE_BUTTON.value).click()
    return driver.find_element(By.XPATH,msg_element).text

def reply_to_message(driver,  msg_element, reply_msg):
    msg = driver.find_element(By.XPATH,msg_element)
    driver.long_press(msg, duration=1000).release().perform()
    driver.find_element(By.XPATH,XPaths.MESSAGING_MESSAGE_HOLD_OPTS_REPLY.value).click()
    driver.find_element(By.XPATH,XPaths.MESSAGING_MESSAGE_FIELD.value).send_keys(reply_msg)
    driver.find_element(By.XPATH,XPaths.MESSAGING_SEND_MESSAGE_BUTTON.value).click()
    driver.hide_keyboard()

def delete_message(driver,  msg_element):
    msg = driver.find_element(By.XPATH,msg_element)
    driver.long_press(msg, duration=1000).release().perform()
    driver.find_element(By.XPATH,XPaths.MESSAGING_MESSAGE_HOLD_OPTS_DELETE.value).click()
    driver.find_element(By.XPATH,XPaths.MESSAGING_MESSAGE_HOLD_OPTS_EXIT.value).click()

def forward_message(driver, msg_element, forward_to):
    msg = driver.find_element(By.XPATH,msg_element.value)
    driver.long_press(msg, duration=1000).release().perform()
    driver.find_element(By.XPATH,XPaths.MESSAGING_MESSAGE_HOLD_OPTS_FORWARD.value).click()
    driver.find_element(By.XPATH,forward_to.value).click()
    driver.find_element(By.XPATH,XPaths.MESSAGING_FORWARD_TO_BACK_BUTTON.value).click()

