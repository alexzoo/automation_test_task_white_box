from base_page import BasePage


class HomePage(BasePage):
    def click_to_login_button(self):
        self.click(id="srf-login-btn")
        return LoginPage(self.driver)


class LoginPage(BasePage):
    def input_credentials(self, email, password):
        self.send_key(email, xpath=".//input[@name='email']")
        self.send_key(password, xpath=".//input[@name='password']")

    def click_to_submit_button(self):
        self.click(xpath=".//button[@data-test='auth-popup__submit']")
        return UserPage(self.driver)


class UserPage(BasePage):
    def click_user_menu_button(self):
        self.click(xpath=".//div[@data-test='header-menu__user']")

    def get_profile_email(self):
        profile_email = self.driver.find_element_by_xpath(".//div[@class='header-dropdown__description']").text
        self.click_user_menu_button()
        return profile_email

    def click_note_link(self):
        self.click(xpath=".//a[@data-ga-label='notes']")
        return NotePage(self.driver)

    def click_project_page_button(self):
        self.click(xpath="//span[@class='tn-projects__add js-ga-createNewProject js-projects-search-bar-create']")
        return ProjectPage(self.driver)

    def logout(self):
        self.click_user_menu_button()
        self.click(xpath="//a[contains(text(),'Log out')]")


class NotePage(BasePage):
    def click_new_note_button(self):
        self.click(xpath=".//button[@data-cream-action='add-note']")

    def fill_note_form(self, note_title, note_description):
        self.send_key(note_title, xpath=".//input[@data-cream-ui='input-title']")
        self.send_key(note_description, xpath=".//textarea[@data-cream-ui='input-note']")

    def click_save_note_button(self):
        self.click(xpath=".//button[@data-cream-action='save']")

    def get_note_name(self):
        note_name = self.driver.find_element_by_xpath(".//span[@class='notes-note-title']").text
        return note_name

    def get_note_description(self):
        note_description = self.driver.find_element_by_xpath("//tbody[@data-cream-ui='items']//tr[1]//td[2]//div[1]//div[2]").text
        return note_description


class ProjectPage(BasePage):

    def fill_project_form(self, domain, project_name):
        self.send_key(domain, xpath="//input[@class='js-pr-watch-domain temp-tn-projects__input']")
        self.send_key(project_name, xpath="//input[@class='js-pr-watch-name temp-tn-projects__input']")

    def click_create_project_button(self):
        self.click(xpath="//button[@class='js-pr-create s-btn -xs -success temp-tn-projects__submit']//span[@class='s-btn__text'][contains(text(),'Create')] ")

    def get_project_title(self):
        title = self.driver.find_element_by_css_selector("div.pr-page__breadcrumbs-wrapper.js-breadcrumbs > div > span").text
        return title

    def delete_project(self, project_name):
        self.click(xpath="//span[@class='s-icon -s -settings']")
        self.click(xpath="//a[@class='js-remove']")
        self.send_key(project_name, xpath="//input[@placeholder='Project name']")
        self.click(xpath="//span[contains(text(),'Delete')]")
        self.wait_element_to_be_clickable(xpath="//span[contains(text(),'Add new project')]")
