from enum import Enum

class XPaths(Enum):
    LOGO = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.ImageView'
    USERNAME_FIELD = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.EditText[1]'
    PASSWORD_FIELD = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.EditText[4]'
    SIGNUP_BUTTON = '//android.widget.Button[@content-desc="Sign Up"]'
    EMAIL_FIELD = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.EditText[2]'
    CONFIRM_PASSWORD_FIELD = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.EditText[5]'
    PHONE_FIELD = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.EditText[3]'
    ERROR_MESSAGE_USERNAME = '//android.view.View[@content-desc="Username is required"]'
    ERROR_MESSAGE_EMAIL  = '//android.view.View[@content-desc="Email is required"]'
    ERROR_MESSAGE_PASSWORD = '//android.view.View[@content-desc="Password must be at least 8 characters"]'
    ERROR_MESSAGE_PHONE = '//android.view.View[@content-desc="Phone number is required"]'
    ERROR_MESSAGE_INVALID_EMAIL = '//android.view.View[@content-desc="Enter a valid email"]'
    ERROR_PASSWORD_DO_NOT_MATCH = '	//android.view.View[@content-desc="Passwords do not match"]'
    REGISTER_INSTRUCTION1 = '//android.view.View[@content-desc="Already have an account? "]'
    REGISTER_INSTRUCTION2 = '//android.widget.Button[@content-desc="Login"]'
    CAPATCHA_CHECK = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.view.View[1]/android.webkit.WebView'
    SIGNUP_VERIFICATION_CODE_FIELD = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[6]/android.view.View'
    SIGNUP_VERIFICATION_CODE_SEND_AGAIN = '//android.widget.Button[@content-desc="Send again"]'
    SIGNUP_VERIFY_CONFIRMATION_CODE_BUTTON = '//android.widget.Button[@content-desc="Verify"]'
    EXCEPTION_WHEN_SUBMIT_VERIFY_CODE = '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout[1]/android.widget.FrameLayout[2]/android.widget.ScrollView/android.widget.FrameLayout[8]/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup'
    LOGIN_BUTTON_IN_REGISTER_FORM = '//android.widget.Button[@content-desc="Login"]'
    LOGIN_FORM_EMAIL_ADDRESS_FIELD = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.EditText[1]'
    LOGIN_FORM_PASSWORD_FIELD = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.EditText[2]'
    LOGIN_FORM_FORGOT_PASSWORD_BUTTON = '//android.view.View[@content-desc="Forgot password?"]'
    LOGIN_FORM_LOGIN_BUTTON = '//android.widget.Button[@content-desc="Log in"]'
    LOGIN_FORM_SIGNUP_BUTTON = '//android.widget.Button[@content-desc="Sign up"]'
    GOOGLE_LOGIN_BUTTON = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.Button[2]'
    GITHUB_LOGIN_BUTTON = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.widget.Button[3]'
    ERROR_DUPLICATE_EMAIL = ''
    ERROR_DUPLICATE_USERNAME = ''
    ERROR_DUPLICATE_PHONE = ''





