import allure
from pages import main_page


@allure.feature("登录")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:

    @allure.feature("登录")
    def test_login_success(self):
        main = main_page.MainPage()
        login_page = main.to_login_page()
        login_page.login("test++2@kucoin.com", "a123456")





