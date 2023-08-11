from pathlib import Path

from webdriver_manager.chrome import ChromeDriverManager
import pytest
from selenium import webdriver
from _pytest.runner import runtestprotocol
from ctreport_selenium.ctlistener import Session, Test


#def pytest_sessionstart(Session):
    #import os
    #if os.path.isdir(str(Path(__file__).parent) + r"/reports/" + "dailyreport/"):
        #import shutil
        #shutil.rmtree(str(Path(__file__).parent) + r"/reports/" + "dailyreport/")

@pytest.fixture(scope="module", autouse=True)
def driver_obj(request, browser, base_url, email, password):
    global driver
    if browser == "chrome":
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        driver = webdriver.Chrome(ChromeDriverManager(version='114.0.5735.90').install())


    Session.start(test_execution_name="Regression Test-Molina CAP Test", path=str(Path(__file__).parent) + r"/reports/",driver=driver,
                  config_file=str(Path(__file__).parent) + "/reportconfig.json")
    driver.maximize_window()
    driver.get(base_url)
    from pages.loginpage import LoginPage
    login = LoginPage(driver)
    login.cap_login(email, password)
    def quit():
        driver.quit()

    request.addfinalizer(quit)
    return driver


def pytest_runtest_protocol(item, nextitem):
    global test
    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.when == 'setup':
            test = item.cls.test
        if report.when == 'call':
            if report.outcome == 'skipped':
                test.broken(report.longrepr.reprcrash.message)
            test.finish()
    temp = ""
    try:
        temp = nextitem.nodeid.split("::")[0]
    except Exception:
        pass
    if nextitem is None or temp != item.nodeid.split("::")[0]:
        Session.end(item.nodeid.split("::")[0].replace("test_", "").replace(".py", "").replace("tests/", ""))
        Session._tests.clear()
        Test._temp_verify_id = 0
        Test._temp_assert_id = 0
        Test._temp_error_id = 0
        Test._temp_screenshot_id = 0
        Test._temp_test_id = 0
        Test._id_li = 0
        Test._id_li = 0
    return False

# def pytest_sessionfinish(session):
#    Session.end()

@pytest.fixture(scope="session")
def base_url(request):
    "pytest fixture for base url"
    return request.config.getoption("-U")

@pytest.fixture(scope="session")
def hip_url(request):
    "pytest fixture for hip url"
    return request.config.getoption("-H")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("-B")

@pytest.fixture(scope="session")
def email(request):
    return request.config.getoption("-E")

@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("-P")

@pytest.fixture(scope="session")
def filepath(request):
    return request.config.getoption("-F")


def pytest_addoption(parser):
    parser.addoption("-U", "--app_url",
                     dest="url",
                     default="https://igrc.inovaare.net/MolinaSSOReplica/loginForm.html",
                     help="The url of the application")

    parser.addoption("-B", "--browser",
                     dest="browser",
                     default="chrome",
                     help="Browser. Valid options are firefox, ie and chrome")

    parser.addoption("-E", "--email",
                     dest="email",
                     default="IA_ComplianceAuditor",
                     help="Valid email id")

    parser.addoption("-P", "--password",
                     dest="password",
                     default="P@s$w04d@1",
                     help="Valid password")
    parser.addoption("-F", "--filepath",
                     dest="filepath",
                     default="D:\Sample GC.xlsx")

