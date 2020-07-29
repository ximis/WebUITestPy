from common import config_load
from pages.main_page import MainPage
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default='k8s',
        help="assign which env to use",
    )
    parser.addoption(
        "--headless",
        action="store",
        help="assign which env to use",
    )


@pytest.fixture(scope="session", autouse=True)
def init(request):
    config_load.init(request.config.option.env)
    if request.config.option.headless is not None:
        config_load.set_options("headless", True)
