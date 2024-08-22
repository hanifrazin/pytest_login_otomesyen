from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture
def setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach",True)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    yield driver
    driver.quit
    
def test_login_positive(setup):
    '''
    Login dengan data valid
    '''
    
    setup.find_element(By.XPATH,"//input[@placeholder='Username']").send_keys('Admin')
    setup.find_element(By.XPATH,"//input[@placeholder='Password']").send_keys('admin123')
    setup.find_element(By.XPATH,"//button[@type='submit']").click()
