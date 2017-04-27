import time
from multiprocessing.pool import Pool

import pytest
from selenium import webdriver
from selenium.webdriver.phantomjs.webdriver import WebDriver


class TestThree(object):

    @pytest.fixture()
    def browser(self):
        driver = webdriver.Chrome()
        driver.set_window_size(1200, 1600)
        return driver

    def test_url_phantom(self, browser: WebDriver):
        time.sleep(1)
        browser.get("http://astrodate.ru/#/") # url associated with button click
        time.sleep(5)
        browser.save_screenshot("image.png")
        time.sleep(20)

    def run_session(self, browser):
        time.sleep(1)
        browser.get("http://astrodate.ru/#/")  # url associated with button click
        time.sleep(20)

    def test_open_sessions(self, browser: WebDriver):
        pool = Pool(10)
        pool.map(self.run_session, [browser for _ in range(10)])
        pool.join()


def run_session(i):
    browser = webdriver.PhantomJS()
    browser.set_window_size(1200, 1600)
    browser.get("http://astrodate.ru/#/")  # url associated with button click
    time.sleep(20)
    browser.close()
    browser.quit()

if __name__ == '__main__':
    pool = Pool(50)
    pool.map(run_session, range(50))
