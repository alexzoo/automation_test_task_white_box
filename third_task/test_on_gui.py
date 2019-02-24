import pytest
from selenium import webdriver
import selenium
from page_objects import HomePage
from hamcrest import assert_that, contains_string, equal_to

'''
    System doesn't allow use mail-randomizer, so I use the constant values of mail and password, 
    with all the settings of my user(in the test will not be present several modal windows).
'''

base_url = "https://www.semrush.com/"
mail_name = 'semrushuitest@gmail.com'
password = '12345'
note_title = 'Test Note'
note_description = 'Test name'
domain = 'http://coffee.com'
project_name = 'Test project'


@pytest.fixture(scope='function')
def driver():
    # Before starting the test, copy chromedriver from http: // www.seleniumhq.org / download / and enter correct PATH.!!
    driver = selenium.webdriver.Chrome("D:\\downloads\\avtotests\\chromedriver.exe")
    driver.get(base_url)
    driver.implicitly_wait(20)
    driver.fullscreen_window()
    yield driver


@pytest.fixture()
def user_page(driver, request):
    home_page = HomePage(driver)
    login_page = home_page.click_to_login_button()

    login_page.input_credentials(mail_name, password)
    user_page = login_page.click_to_submit_button()

    def close_teardown():
        driver.quit()

    request.addfinalizer(close_teardown)

    return user_page


class TestForSemrush:
    def test_login_as_semrush_user(self, user_page):
        user_page.click_user_menu_button()

        assert_that(user_page.get_profile_email(), contains_string('semrushui'))

    def test_create_new_notes(self, user_page):
        note_page = user_page.click_note_link()

        note_page.click_new_note_button()
        note_page.fill_note_form(note_title, note_description)
        note_page.click_save_note_button()

        assert_that(note_page.get_note_name(), equal_to(note_title))
        assert_that(note_page.get_note_description(), equal_to(note_description))

    def test_create_new_project(self, user_page):
        project_page = user_page.click_project_page_link()
        project_page._delete_project_if_exists(project_name)

        project_page.add_new_project_button()
        project_page.fill_project_form(domain, project_name)
        project_page.click_create_project_button()

        assert_that(project_page.get_project_title(), contains_string(project_name))