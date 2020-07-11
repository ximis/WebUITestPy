from common import config_load
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default='k8s',
        help="assign which env to use",
    )


@pytest.fixture(scope="session", autouse=True)
def init(request):
    config_load.init(request.config.option.env)


