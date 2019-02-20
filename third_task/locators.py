class HomePageLocators(object):
    LOGIN = 'srf-login-btn'
    EMAILFIELD = ".//input[@name='email']"
    PASSWORDFIELD = ".//input[@name='password']"
    SUBMIT = ".//button[@data-test='auth-popup__submit']"


class UserPageLocators(object):
    USERMENU = ".//div[@data-test='header-menu__user']"
    USEREMAIL = ".//div[@class='header-dropdown__description']"
    NOTELINK = ".//a[@data-ga-label='notes']"
    PROJECTPAGELINK = "//a[contains(text(),'Projects')]"


class NotePageLocators(object):
    NEWNOTEBUTTON = ".//button[@data-cream-action='add-note']"
    NOTETITLEFIELD = ".//input[@data-cream-ui='input-title']"
    NOTEDESCRIPTIONFIELD = ".//textarea[@data-cream-ui='input-note']"
    SAVENOTEBUTTON = ".//button[@data-cream-action='save']"
    NOTENAME = ".//span[@class='notes-note-title']"
    NEWNOTEDESCRIPTION = "//tbody[@data-cream-ui='items']//tr[1]//td[2]//div[1]//div[2]"


class ProjectPageLocators(object):
    ADDNEWPROJECTBUTTON = "//span[contains(text(),'Add new project')]"
    DOMAINFIELD = "//input[@placeholder='Enter project domain']"
    PROJECTNAMEFIELD = "//input[@placeholder='Enter project name']"
    NEWPROJECTBUTTON = "//span[contains(text(),'Create project')]"
    SETTINGS = "//div[@class='sr-infomenu-title']"
    PROJECTTITLE = "//div[@class='pr-page__title']//span[1]"
    PROJECTEXIST = "//div[@class='Styles__body___2zR9D']"
    REMOVEBUTTON = "//a[@class='js-remove']"
    DELETEPROJECTNAME = "//input[@placeholder='Project name']"
    DELETEBUTTON = "//span[contains(text(),'Delete')]"
