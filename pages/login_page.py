from selenium.webdriver.common.by import By

from .base_page import BasePage
from common import config_load


class LoginPage(BasePage):
    def __init__(self):
        super().__init__()

    def login(self, name=None, passowrd=None):
        if name is None:
            name = config_load.get_env().get("username")
        if passowrd is None:
            passowrd = config_load.get_env().get("password")
        self.send_keys(self.name.by, self.name.locator, name)
        self.send_keys(self.password.by, self.password.locator, passowrd)
        self.click(self.login_btn.by, self.login_btn.locator)
    





