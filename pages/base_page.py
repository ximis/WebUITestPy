from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Chrome,ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
import time

from common import config_load

import sys

RETRY_COUNT = 3


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
        options = ChromeOptions()
        options.page_load_strategy = "none"
        if config_load.get_options().get("headless"):
            options.add_argument("--window-size=1280,940")
            options.add_argument("--start-maximized")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--headless')
            options.add_experimental_option("mobileEmulation", {
                "userAgent":
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"})
        if 'linux' in sys.platform:
            self.driver = Chrome(options=options)
        else:
            self.driver = Chrome(executable_path='../resources/drivers/chromedriver', options=options)
        self.driver.maximize_window()
        BasePage.driver = self.driver
        self.page_bottom()
        self.page_top()
        self.driver.implicitly_wait(5)

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
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        self.wait = WebDriverWait(self.driver, 15, ignored_exceptions=ignored_exceptions)

    def find_element(self, by, locator):
        self.wait.until(expected_conditions.visibility_of_element_located((by, locator)))
        return self.driver.find_element(by, locator)

    # def click(self, by, locator):
    #     self.wait.until(expected_conditions.element_to_be_clickable((by, locator)))
    #     self.driver.find_element(by, locator).click()

    def click(self, by, locator):
        count = 1
        while count <= RETRY_COUNT:
            try:
                self.wait.until(expected_conditions.element_to_be_clickable((by, locator)))
                self.driver.find_element(by, locator).click()
                break
            except Exception as e:
                time.sleep(3)
                count += 1
                if count > RETRY_COUNT:
                    raise e

    def move_to_elements(self, by, locator):
        self.wait.until(expected_conditions.visibility_of_element_located((by, locator)))
        ActionChains(self.driver).move_to_element(self.driver.find_element(by, locator)).perform()

    def find_elements(self, by, locator):
        self.wait.until(expected_conditions.visibility_of_element_located((by, locator)))
        return self.driver.find_elements(by, locator)

    def send_keys(self, by, locator, data):
        self.wait.until(expected_conditions.element_to_be_clickable((by, locator)))
        # self.driver.find_element(by, locator).clear()  # 在发送之前，清理。 在个在某些情况下并不能很好的工作，采用下面这种方式
        self.driver.find_element(by, locator).send_keys(Keys.CONTROL, 'a')  #工作正常
        self.driver.find_element(by, locator).send_keys(data)

    def get_property(self, by, locator, name):
        return self.find_element(by, locator).get_property(name)

    def get_text(self, by, locator):
        return self.find_element(by, locator).text

    def get_tag_name(self, by, locator):
        return self.find_element(by, locator).tag_name

    def page_down(self):
        self.driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_DOWN)

    def page_up(self):
        self.driver.find_element_by_tag_name('html').send_keys(Keys.PAGE_UP)

    def page_slightly_down(self):
        self.driver.find_element_by_tag_name('html').send_keys(Keys.ARROW_DOWN)

    def page_slightly_up(self):
        self.driver.find_element_by_tag_name('html').send_keys(Keys.ARROW_UP)

    def set_page_position(self, x, y):
        self.driver.execute_script("window.scrollTo(%s, %s)" % (x, y))

    def page_top(self):
        self.set_page_position(0, 0)

    def page_bottom(self):
        self.set_page_position(0, 10000)

    def quit(self):
        self.driver.quit()
        BasePage.driver = None

    def isElementExist(self, by, locator):
        flag = True
        try:
            self.find_element(by, locator)
            return flag
        except:
            flag = False
            return flag

    def page_back(self):
        url = self.driver.current_url
        self.driver.back()
        self.wait.until_not(expected_conditions.url_to_be(url))
        self.wait.until(expected_conditions.presence_of_all_elements_located(("xpath", "html")))
        # self.wait.until(expected_conditions.visibility_of_all_elements_located(("xpath", "html")))
        self.driver.get(self.driver.current_url)

    def change_window(self):
        time.sleep(1)
        handles = self.driver.window_handles
        index_handle = self.driver.current_window_handle
        for handle in handles:
            if handle != index_handle:
                self.driver.switch_to.window(handle)
            else:
                continue

    def close_window(self):
        time.sleep(1)
        self.driver.close()
        handles = self.driver.window_handles
        for handle in handles:
            self.driver.switch_to.window(handle)
            break

    def get_attribute(self, by, locator, name):
        return self.find_element(by, locator).get_attribute(name)

    def get_url(self):
        return self.driver.current_url
