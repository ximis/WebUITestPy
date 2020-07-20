from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from common import config_load


class BasePage:
    driver = None

    def __init__(self):
        self.driver: Chrome = None
        self.wait: WebDriverWait = None
        if BasePage.driver is None:
            self._start_driver()
        else:
            self.driver = BasePage.driver

        self._init_wait()
        self._init_page()

    def _start_driver(self):
        self.driver = Chrome(executable_path='../resources/drivers/chromedriver')
        BasePage.driver = self.driver
        self.driver.implicitly_wait(10)

    def _init_page(self):
        data = config_load.get_page(self.__module__.split(".")[-1])

        class Locator:
            def __init__(self, data):
                self.by = data['by']
                self.locator = data['locator']

        if data is not None:
            for i in data:
                self.__dict__[i] = Locator(data[i])

    def __getattr__(self, item, ):
        raise ValueError("can't find element")

    def _init_wait(self):
        self.wait = WebDriverWait(self.driver, 30)

    def find_element(self, by, locator):
        self.wait.until(expected_conditions.visibility_of_element_located((by, locator)))
        return self.driver.find_element(by, locator)

    def click(self, by, locator):
        self.wait.until(expected_conditions.element_to_be_clickable((by, locator)))
        self.driver.find_element(by, locator).click()

    def send_keys(self, by, locator, data):
        self.wait.until(expected_conditions.element_to_be_clickable((by, locator)))
        self.driver.find_element(by, locator).send_keys(data)

    def get_property(self, by, locator, name):
        return self.find_element(by, locator).get_property(name)

    def get_text(self, by, locator):
        return self.find_element(by, locator).text

    def get_tag_name(self, by, locator):
        return self.find_element(by, locator).tag_name

    def quit(self):
        self.driver.quit()
        BasePage.driver = None
