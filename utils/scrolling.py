import time

def scroll_down(driver):
    """
    Scrolls the screen vertically by performing a swipe action using TouchAction.
    Adjust the scroll direction and distance as per your requirements.
    """
    size = driver.get_window_size()
    print(f"Window size: {size}")

    start_x = size['width'] / 2
    start_y = size['height'] * 0.3
    end_y = size['height'] * 0.2
    driver.swipe(start_x, start_y, start_x, end_y, 400)


def scroll_down_until_element_found(driver, by, value, max_scrolls=5):
    """
    Scrolls the screen vertically until the element is found.
    """
    scroll_count = 0
    while scroll_count < max_scrolls:
        try:
            element = driver.find_element(by, value)
            if element.is_displayed():
                print(f"Element found: {element}")
                return True
        except Exception as e:
            print(f"Element not found, scrolling... Exception: {e}")

        scroll_down(driver)
        scroll_count += 1
        print(f"Scroll count: {scroll_count}")
        time.sleep(1)
    return False

def scroll_up_until_element_found(driver, by, value, max_scrolls=5):
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
            element = driver.find_element(by, value)
            if element.is_displayed():
                print(f"Element found: {element}")
                return True
        except Exception as e:
            print(f"Element not found, scrolling...")

        scroll_up(driver)
        scroll_count += 1
        time.sleep(1)
    return False

def scroll_up(driver):
    """
    Scrolls the screen vertically by performing a swipe action using TouchAction.
    Adjust the scroll direction and distance as per your requirements.
    """
    size = driver.get_window_size()
    start_x = size['width'] / 2
    start_y = size['height'] * 0.2
    end_y = size['height'] * 0.3
    driver.swipe(start_x, start_y, start_x, end_y, 400)
