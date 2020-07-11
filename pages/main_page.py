from selenium.webdriver.common.by import By

from common import config_load
from .base_page import BasePage
from .login_page import LoginPage


class MainPage(BasePage):
    def __init__(self):
        super().__init__()
        self.driver.get(config_load.get_env())

    def to_login_page(self):
        self.click(self.login.by, self.login.locator)
        return LoginPage(self.driver)


