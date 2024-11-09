import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

def scroll_until_element_found(driver, by, value, max_scrolls=5):
    """
    Scrolls the screen vertically until the element is found.
    :param driver: Appium driver instance
    :param by: The locator strategy (e.g., By.ID, By.XPATH)
    :param value: The value to locate the element
    :param max_scrolls: Maximum number of scrolls before stopping
    :return: True if element is found, False otherwise
    """
    scroll_count = 0
    while scroll_count < max_scrolls:
        try:
            # Try to find the element
            element = driver.find_element(by, value)
            if element.is_displayed():
                print(f"Element found: {element}")
                return True  # Element found
        except Exception as e:
            print(f"Element not found, scrolling...")

        # Perform a scroll (swipe action)
        scroll(driver)
        scroll_count += 1
        time.sleep(0.5)  # Optional, just to give some time for scrolling
    return False  # Element not found after max scrolls

def scroll(driver):
    """
    Scrolls the screen vertically by performing a swipe action using TouchAction.
    Adjust the scroll direction and distance as per your requirements.
    """
    size = driver.get_window_size()
    start_x = size['width'] / 2  # Start in the center of the screen horizontally
    start_y = size['height'] * 0.4  # Start near the bottom of the screen
    end_y = size['height'] * 0.2  # End near the top of the screen

    # Using TouchAction to perform a swipe (scroll)
    action = TouchAction(driver)
    print(start_x, start_y,  end_y, sep='\t')
    action.press(x=start_x, y=start_y).move_to(x=start_x, y=end_y).release().perform()
