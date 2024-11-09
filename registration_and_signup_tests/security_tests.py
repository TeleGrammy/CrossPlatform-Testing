import unittest
from appium import webdriver


class InputValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capabilities = {
            "platformName": 'Android',
            "deviceName": '146ce6c8',
            "app": r'C:\Users\20115\Downloads\app-release.apk'
        }
        cls.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', capabilities)
        cls.driver.implicitly_wait(50)

    def test_sql_injection_prevention(self):
        # Attempt SQL injection in input fields
        sql_injection_string = "test' OR '1'='1"
        self.register_user("sql_inject_user", "sql_inject@example.com", sql_injection_string)
        self.assertTrue(self.check_error_message("Invalid input detected."), "SQL injection attempt was not prevented.")

    def test_xss_attack_prevention(self):
        # Attempt XSS injection in input fields
        xss_string = "<script>alert('XSS')</script>"
        self.register_user("xss_user", "xss@example.com", xss_string)
        self.assertTrue(self.check_error_message("Invalid input detected."), "XSS attempt was not prevented.")

    def test_csrf_token_presence(self):
        # Verify presence of CSRF token in form submission
        csrf_token = self.driver.find_element_by_xpath('//input[@name="csrf_token"]').get_attribute("value")
        self.assertIsNotNone(csrf_token, "CSRF token is missing in form submission.")

    def test_html_entity_decoding(self):
        # Test input with HTML entities to ensure proper decoding
        html_entity_string = "&lt;script&gt;alert('test')&lt;/script&gt;"
        self.register_user("entity_user", "entity@example.com", html_entity_string)
        self.assertTrue(self.check_error_message("Invalid input detected."),
                        "HTML entity injection not correctly handled.")

    def test_url_encoded_characters(self):
        # Test input with URL-encoded characters
        url_encoded_string = "%3Cscript%3Ealert%28%27test%27%29%3C%2Fscript%3E"
        self.register_user("url_encoded_user", "urlencoded@example.com", url_encoded_string)
        self.assertTrue(self.check_error_message("Invalid input detected."),
                        "URL-encoded XSS injection was not prevented.")

    def register_user(self, username, email, password):
        # Helper function to register a user
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]').send_keys(username)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Email"]').send_keys(email)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Password"]').send_keys(password)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()

    def check_error_message(self, expected_message):
        # Helper function to verify specific error messages
        error_element = self.driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Error Message']")
        return expected_message in error_element.text

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
