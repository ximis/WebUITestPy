import allure
import pytest
from pages import baidu_search_page


@allure.feature("搜索")
class TestBaiduSearch:
    # @classmethod
    # def setup_class(cls):
    #     page = baidu_search_page.BaiduSearchPage()
    #     page.search("selenium")
    #     assert "seleniumsdfasfdaf" in page.get_url()

    @pytest.fixture(scope="class")
    def page(self):
        page = baidu_search_page.BaiduSearchPage()
        yield page
        page.quit()

    @allure.story("search and check url")
    def test_search(self, page):
        page.search("selenium")
        assert "selenium" in page.get_url()

    @allure.story("search 2")
    def test_search2(self, page):
        page.search("selenium")
        assert "selenium" not in page.get_url()

