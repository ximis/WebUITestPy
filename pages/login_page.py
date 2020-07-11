from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def login(self, name, passowrd):
        self.send_keys(self.name.by, self.name.locator, name)
        self.send_keys(self.password.by, self.password.locator, passowrd)
        self.click(self.login_btn.by, self.login_btn.locator)





