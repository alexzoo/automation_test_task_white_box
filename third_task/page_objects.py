
from base_page import BasePage
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class HomePage(BasePage):
    LOGIN = 'srf-login-btn'

    def click_to_login_button(self):
        self.click(id=self.LOGIN)
        return LoginPage(self.driver)


class LoginPage(BasePage):
    EMAILFIELD = ".//input[@name='email']"
    PASSWORDFIELD = ".//input[@name='password']"
    SUBMIT = ".//button[@data-test='auth-popup__submit']"

    def input_credentials(self, email, password):
        self.send_key(email, xpath=self.EMAILFIELD)
        self.send_key(password, xpath=self.PASSWORDFIELD)

    def click_to_submit_button(self):
        self.click(xpath=self.SUBMIT)
        return UserPage(self.driver)


class UserPage(BasePage):
    USERMENU = ".//div[@data-test='header-menu__user']"
    USEREMAIL = ".//div[@class='header-dropdown__description']"
    NOTELINK = ".//a[@data-ga-label='notes']"
    PROJECTPAGELINK = "//a[contains(text(),'Projects')]"

    def click_user_menu_button(self):
        self.click(xpath=self.USERMENU)

    def get_profile_email(self):
        profile_email = self.get_web_element(self.USEREMAIL)
        return profile_email.text

    def click_note_link(self):
        self.click(xpath=self.NOTELINK)
        return NotePage(self.driver)

    def click_project_page_link(self):
        self.wait_element_to_be_clickable(xpath=self.PROJECTPAGELINK)
        self.click(xpath=self.PROJECTPAGELINK)
        return ProjectPage(self.driver)


class NotePage(BasePage):
    NEWNOTEBUTTON = ".//button[@data-cream-action='add-note']"
    NOTETITLEFIELD = ".//input[@data-cream-ui='input-title']"
    NOTEDESCRIPTIONFIELD = ".//textarea[@data-cream-ui='input-note']"
    SAVENOTEBUTTON = ".//button[@data-cream-action='save']"
    NOTENAME = ".//span[@class='notes-note-title']"
    NEWNOTEDESCRIPTION = "//tbody[@data-cream-ui='items']//tr[1]//td[2]//div[1]//div[2]"

    def click_new_note_button(self):
        self.click(xpath=self.NEWNOTEBUTTON)

    def fill_note_form(self, note_title, note_description):
        self.send_key(note_title, xpath=self.NOTETITLEFIELD)
        self.send_key(note_description, xpath=self.NOTEDESCRIPTIONFIELD)

    def click_save_note_button(self):
        self.click(xpath=self.SAVENOTEBUTTON)

    def get_note_name(self):
        note_name = self.get_web_element(xpath=self.NOTENAME)
        return note_name.text

    def get_note_description(self):
        self.wait_element_to_be_clickable(xpath=UserPage.USERMENU)
        note_description = self.get_web_element(xpath=self.NEWNOTEDESCRIPTION)
        return note_description.text


class ProjectPage(BasePage):
    ADDNEWPROJECTBUTTON = "//span[contains(text(),'Add new project')]"
    DOMAINFIELD = "//input[@placeholder='Enter project domain']"
    PROJECTNAMEFIELD = "//input[@placeholder='Enter project name']"
    NEWPROJECTBUTTON = "//span[contains(text(),'Create project')]"
    ABOUTLINK = "//a[@class='s-widget__link'"
    SETTINGS = "//div[@class='sr-infomenu-title']"
    PROJECTTITLE = "//div[@class='pr-page__title']//span[1]"
    PROJECTEXIST = "//div[@class='Styles__body___2zR9D']"
    REMOVEBUTTON = "//a[contains(text(),'Delete')]"
    DELETEPROJECTNAME = "//input[@placeholder='Project name']"
    DELETEBUTTON = "//span[contains(text(),'Delete project')]"
    CREATEDSETTINGS = "//*[@class='sc-1_4_7-icon _1oEeA23r9xDuBmcet_boK']"


    def add_new_project_button(self):
        self.wait_element_to_be_clickable(xpath=self.ADDNEWPROJECTBUTTON)
        self.click(xpath=self.ADDNEWPROJECTBUTTON)

    def fill_project_form(self, domain, project_name):
        self.send_key(domain, xpath=self.DOMAINFIELD)
        self.send_key(project_name, xpath=self.PROJECTNAMEFIELD)

    def click_create_project_button(self):
        self.click(xpath=self.NEWPROJECTBUTTON)

    def get_project_title(self):
        self.wait_element_to_be_clickable(xpath=self.SETTINGS)
        title = self.get_web_element(xpath=self.PROJECTTITLE)
        return title.text

    def _delete_project_if_exists(self, project_name):
        try:
            self.get_web_element(xpath=self.PROJECTEXIST)
        except NoSuchElementException:
            return

        self.wait_element_to_be_clickable(xpath=self.PROJECTEXIST)
        element = self.get_web_element(xpath=self.PROJECTEXIST)
        ActionChains(self.driver).move_to_element(element).perform()
        self.wait_element_to_be_clickable(xpath=self.CREATEDSETTINGS)
        self.click(xpath=self.CREATEDSETTINGS)
        self.click(xpath=self.REMOVEBUTTON)
        self.send_key(project_name, xpath=self.DELETEPROJECTNAME)
        self.click(xpath=self.DELETEBUTTON)
        self.wait_element_to_be_clickable(xpath=UserPage.USERMENU)

