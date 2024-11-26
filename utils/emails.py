import imaplib
import email
import re

class EmailVerification:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.mail = None

    def connect(self):
        """Connect to the email server."""
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.email_address, self.password)
        self.mail.select('inbox')

    def search_email(self, sender_email):
        """Search for emails from a specific sender."""
        status, messages = self.mail.search(None, 'FROM', sender_email)
        if status != "OK" or not messages[0]:
            raise Exception("No emails found from the specified sender.")
        email_ids = messages[0].split()
        return email_ids

    @classmethod
    def get_verification_code(cls, email_address, password, sender_email):
        """Fetch and return the latest verification code from the specified sender."""
        instance = cls(email_address, password)
        instance.connect()
        email_ids = instance.search_email(sender_email)

        latest_email_id = email_ids[-1]
        status, msg_data = instance.mail.fetch(latest_email_id, '(RFC822)')
        if status != "OK":
            raise Exception("Failed to fetch the email.")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_body = part.get_payload(decode=True).decode()
                    match = re.search(r'\b\d{6}\b', email_body)
                    if match:
                        return match.group(0)
        raise Exception("Verification code not found in the email.")