from .base_page import BasePage
from common import config_load

'''
这个类替代了main page，是我用来试验各种功能的。
'''


class BaiduSearchPage(BasePage):
    def __init__(self):
        super().__init__()
        self.driver.get(config_load.get_env().get("url"))

    def search(self, data):
        self.send_keys(self.search_input.by, self.search_input.locator, data)
        self.click(self.search_btn.by, self.search_btn.locator)
