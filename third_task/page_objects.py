from base_page import BasePage
from locators import HomePageLocators, UserPageLocators, NotePageLocators, ProjectPageLocators


class HomePage(BasePage):
    def click_to_login_button(self):
        self.click(id=HomePageLocators.LOGIN)
        return LoginPage(self.driver)


class LoginPage(BasePage):
    def input_credentials(self, email, password):
        self.send_key(email, xpath=HomePageLocators.EMAILFIELD)
        self.send_key(password, xpath=HomePageLocators.PASSWORDFIELD)

    def click_to_submit_button(self):
        self.click(xpath=HomePageLocators.SUBMIT)
        return UserPage(self.driver)


class UserPage(BasePage):

    def click_user_menu_button(self):
        self.click(xpath=UserPageLocators.USERMENU)

    def get_profile_email(self):
        profile_email = self.get_web_element(UserPageLocators.USEREMAIL)
        return profile_email.text

    def click_note_link(self):
        self.click(xpath=UserPageLocators.NOTELINK)
        return NotePage(self.driver)

    def click_project_page_link(self):
        self.wait_element_to_be_clickable(xpath=UserPageLocators.PROJECTPAGELINK)
        self.click(xpath=UserPageLocators.PROJECTPAGELINK)
        return ProjectPage(self.driver)


class NotePage(BasePage):
    def click_new_note_button(self):
        self.click(xpath=NotePageLocators.NEWNOTEBUTTON)

    def fill_note_form(self, note_title, note_description):
        self.send_key(note_title, xpath=NotePageLocators.NOTETITLEFIELD)
        self.send_key(note_description, xpath=NotePageLocators.NOTEDESCRIPTIONFIELD)

    def click_save_note_button(self):
        self.click(xpath=NotePageLocators.SAVENOTEBUTTON)

    def get_note_name(self):
        note_name = self.get_web_element(xpath=NotePageLocators.NOTENAME)
        return note_name.text

    def get_note_description(self):
        self.wait_element_to_be_clickable(xpath=UserPageLocators.USERMENU)
        note_description = self.get_web_element(xpath=NotePageLocators.NEWNOTEDESCRIPTION)
        return note_description.text


class ProjectPage(BasePage):
    def __init__(self, driver):
        project_name = 'Test project'
        super().__init__(driver)
        self._delete_project_if_exists(project_name)

    def add_new_project_button(self):
        self.wait_element_to_be_clickable(xpath=ProjectPageLocators.ADDNEWPROJECTBUTTON)
        self.click(xpath=ProjectPageLocators.ADDNEWPROJECTBUTTON)

    def fill_project_form(self, domain, project_name):
        self.send_key(domain, xpath=ProjectPageLocators.DOMAINFIELD)
        self.send_key(project_name, xpath=ProjectPageLocators.PROJECTNAMEFIELD)

    def click_create_project_button(self):
        self.click(xpath=ProjectPageLocators.NEWPROJECTBUTTON)

    def get_project_title(self):
        self.wait_element_to_be_clickable(xpath=ProjectPageLocators.SETTINGS)
        title = self.get_web_element(xpath=ProjectPageLocators.PROJECTTITLE)
        return title.text

    def _delete_project_if_exists(self, project_name):
        if self.get_web_element(xpath=ProjectPageLocators.PROJECTEXIST).is_displayed():
            self.wait_element_to_be_clickable(xpath=ProjectPageLocators.PROJECTEXIST)
            self.click(xpath=ProjectPageLocators.PROJECTEXIST)
            self.wait_element_to_be_clickable(xpath=ProjectPageLocators.SETTINGS)
            self.click(xpath=ProjectPageLocators.SETTINGS)
            self.click(xpath=ProjectPageLocators.REMOVEBUTTON)
            self.send_key(project_name, xpath=ProjectPageLocators.DELETEPROJECTNAME)
            self.click(xpath=ProjectPageLocators.DELETEBUTTON)
            self.wait_element_to_be_clickable(xpath=UserPageLocators.USERMENU)
