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
    REGISTER_INSTRUCTION1 = '//android.view.View[@content-desc="Already have an account? "]'
    REGISTER_INSTRUCTION2 = '//android.widget.Button[@content-desc="Login"]'
    CAPATCHA_CHECK = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.view.View[1]/android.webkit.WebView'