from selenium.webdriver.common.by import By

from common import config_load
from .base_page import BasePage
from .login_page import LoginPage
from .assets_page import AssetsPage


class MainPage(BasePage):
    def __init__(self):
        super().__init__()
        self.driver.get(config_load.get_env().get("url"))

    def to_login_page(self):
        self.click(self.login.by, self.login.locator)
        return LoginPage()

    def to_assets_page(self):
        self.click(self.assets.by, self.assets.locator)
        return AssetsPage()

    def get_assets_text(self):
        '''
        获取资产按钮，用来表示资产按钮存在
        :return:
        '''
        return self.get_text(self.assets.by, self.assets.locator)


