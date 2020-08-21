from common import config_load
from pages.main_page import MainPage
import pytest
import time
from datetime import datetime
import allure
import os

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


# set up a hook to be able to check if a test has failed
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


# check if a test has failed
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            # find a way to get driver
            driver = request.node.funcargs['page'].driver
            take_screenshot(driver, request.node.nodeid)
            print("executing test failed", request.node.nodeid)


# make a screenshot with a name of the test, date and time
def take_screenshot(driver, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace("/", "_").replace("::", "__")
    driver.save_screenshot(file_name)
    allure.attach.file(file_name, attachment_type=allure.attachment_type.PNG)
    os.remove(file_name)
