from common.common_imports import *

load_dotenv()

class ScenariosOneOnOneMessaging(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capabilities = {
            "platformName": Connect.PLATFORM_NAME.value,
            "deviceName": Connect.DEVICE_NAME_TABLET.value,
            "app": Connect.APP.value
        }
        cls.driver = webdriver.Remote(Connect.COMMAND_EXE.value, capabilities)
        cls.driver.implicitly_wait(50)

    def test_01(self):
        pass


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()