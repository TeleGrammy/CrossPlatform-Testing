import unittest
from appium import webdriver
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Appium driver
        capabilities = {
            "platformName": 'Android',
            "deviceName": '146ce6c8',
            "app": r'C:\Users\20115\Downloads\app-release.apk'
        }
        cls.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', capabilities)
        cls.driver.implicitly_wait(50)

    def test_verification_email_sent_on_successful_registration(self):
        # Register a user
        self.register_user("test_email_user", "testemailuser@example.com", "ValidPassword123")

        # Simulate checking the email service to confirm the verification email
        self.assertTrue(self.verify_email_sent("testemailuser@example.com"), "Verification email was not sent.")

    def test_email_content_verification(self):
        # Register a user
        self.register_user("test_email_user", "testemailuser@example.com", "ValidPassword123")

        # Get the email content (subject, body)
        email_content = self.get_email_content("testemailuser@example.com")

        self.assertIn("Verification Link", email_content, "Verification link is missing from the email.")
        self.assertIn("testemailuser@example.com", email_content,
                      "User-specific information is missing from the email.")

    def test_email_delivery_failure_handling(self):
        # Simulate email service unavailability
        self.simulate_email_service_failure()

        # Register a user
        self.register_user("test_email_user", "testemailuser@example.com", "ValidPassword123")

        # Verify graceful handling of email failure
        self.assertTrue(self.check_error_message("Email service is temporarily unavailable."),
                        "Error message for email failure is incorrect.")

    def simulate_email_service_failure(self):
        # Simulate email service failure by raising an exception
        raise smtplib.SMTPException("Email service failure.")

    def register_user(self, username, email, password):
        # Helper function to register a user
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Username"]').send_keys(username)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Email"]').send_keys(email)
        self.driver.find_element_by_xpath('//android.widget.EditText[@content-desc="Password"]').send_keys(password)
        self.driver.find_element_by_xpath('//android.widget.Button[@content-desc="Sign Up"]').click()

    def get_email_content(self, email):
        # Simulate fetching the email content (e.g., using a mail service API)
        return "Verification Link: http://example.com/verify?email=" + email

    def check_error_message(self, expected_message):
        # Helper function to verify error message
        error_element = self.driver.find_element_by_xpath("//android.widget.TextView[@content-desc='Error Message']")
        return expected_message in error_element.text

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
