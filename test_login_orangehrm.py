from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

url = 'https://opensource-demo.orangehrmlive.com/web/index.php'

@pytest.fixture
def setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach",True)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get(url+"/auth/login")
    yield driver
    driver.quit()
    
def test_login_positive(setup):
    '''
    Login dengan data valid
    '''
    
    setup.find_element(By.XPATH,"//input[@placeholder='Username']").send_keys('Admin')
    setup.find_element(By.XPATH,"//input[@placeholder='Password']").send_keys('admin123')
    setup.find_element(By.XPATH,"//button[@type='submit']").click()
    
    dashboard_header = setup.find_element(By.XPATH,"//h6[@class='oxd-text oxd-text--h6 oxd-topbar-header-breadcrumb-module']").text
    dashboard_sidebar = setup.find_element(By.XPATH,"//a[@class='oxd-main-menu-item active']//span[@class='oxd-text oxd-text--span oxd-main-menu-item--name']").text
    elementds = setup.find_element(By.XPATH,"//a[@class='oxd-main-menu-item active']")
    
    expect_menu = 'Dashboard'
    login_url = setup.current_url
    expect_login_url = url+'/dashboard/index'
    class_ds = elementds.get_attribute("class")
    
    assert login_url == expect_login_url
    assert dashboard_header == expect_menu
    assert dashboard_sidebar == expect_menu
    assert "active" in class_ds.split(), "Class 'active' tidak ditemukan"

case_invalid_creds = [
    ('sipalingadmin','admin123','Invalid credentials',True),
    ('Admin','P@ssw0rd123','Invalid credentials',True),
    ('sipalingadmin','P@ssw0rd123','Invalid credentials',True)
]

@pytest.mark.parametrize('username,password,error_notif,is_element',case_invalid_creds)    
def test_login_invalid_credentials(setup,username,password,error_notif,is_element):
    '''
    Login dengan invalid credential
    '''
    
    setup.find_element(By.XPATH,"//input[@placeholder='Username']").send_keys(username)
    setup.find_element(By.XPATH,"//input[@placeholder='Password']").send_keys(password)
    setup.find_element(By.XPATH,"//button[@type='submit']").click()
    
    validasi_msg = setup.find_element(By.XPATH,"//body/div[@id='app']/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/p[1]").text
    assert validasi_msg == error_notif
    error_element = setup.find_element(By.XPATH,"//body/div[@id='app']/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]").is_displayed()
    assert error_element == is_element

case_empty_creds = [
    ('','admin123','Required',True),
    ('Admin','','Required',True),
    ('','','Required',True)
]

@pytest.mark.parametrize('username,password,notif_error,is_element',case_empty_creds)    
def test_login_empty_credentials(setup,username,password,notif_error,is_element):
    '''
    Login dengan empty credential
    '''
    
    setup.find_element(By.XPATH,"//input[@placeholder='Username']").send_keys(username)
    setup.find_element(By.XPATH,"//input[@placeholder='Password']").send_keys(password)
    setup.find_element(By.XPATH,"//button[@type='submit']").click()
    
    validasi_msg = setup.find_element(By.XPATH,"//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message']").text
    assert validasi_msg == notif_error
    red_field = setup.find_element(By.XPATH,"//input[@class='oxd-input oxd-input--active oxd-input--error']").is_displayed()
    assert red_field == is_element
    