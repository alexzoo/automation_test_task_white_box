from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click(self, xpath=None, id=None):
        if id is not None:
            self.driver.find_element_by_id(id).click()
        elif xpath is not None:
            self.driver.find_element_by_xpath(xpath).click()

    def wait_element_to_be_clickable(self, xpath):
        if xpath:
            WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(
                (By.XPATH, xpath)))

    def send_key(self, text, xpath):
        if xpath:
            self.driver.find_element_by_xpath(xpath).send_keys(text)

    def get_web_element(self, xpath):
        if xpath:
            return self.driver.find_element_by_xpath(xpath)
