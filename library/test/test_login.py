from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLogin:
    def setup_method(self):
        self.driver = webdriver.Chrome()

    def test_open_homepage(self):
        self.driver.get("http://127.0.0.1:8000/")
        assert self.driver.title == "Home | Library"

    def test_open_login_page(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        assert self.driver.title == "Log in | Library"

    def test_login_form_fields(self):
        self.driver.get("http://127.0.0.1:8000/auth/login/")
        assert self.driver.title == "Log in | Library"
        email = self.driver.find_element(By.ID, "email")
        assert email.is_displayed()
        password = self.driver.find_element(By.ID, "password")
        assert password.is_displayed()  

    def test_enter_email_and_password(self):
        self.driver.get("http://127.0.0.1:8000/auth/login/")
        assert self.driver.title == "Log in | Library"
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        email.send_keys("test@gmail.com")
        password.send_keys("testpassword")
        assert email.get_attribute("value") == "test@gmail.com"
        assert password.get_attribute("value") == "testpassword"

    def test_login_with_valid_credentials(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        assert self.driver.title == "Log in | Library"
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        email.send_keys("user1@gmail.com")
        password.send_keys("user1user1")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[normalize-space()='Logout']")
            )
        )

        assert logout_button.is_displayed()
        assert self.driver.title == "Home | Library"

    def test_logout(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        assert self.driver.title == "Log in | Library"
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        email.send_keys("user1@gmail.com")
        password.send_keys("user1user1")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[normalize-space()='Logout']")
            )
        )
        logout_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.all_of(
                EC.title_is("Home | Library"),
                EC.invisibility_of_element_located(
                    (By.XPATH, "//button[normalize-space()='Logout']")
                )
            )
        )
        login_link = self.driver.find_element(By.LINK_TEXT, "Login")
        assert login_link.is_displayed()

    def test_login_with_invalid_credentials(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        assert self.driver.title == "Log in | Library"
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        email.send_keys("user1@gmail.com")
        password.send_keys("useruser")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//button[normalize-space()='Logout']")
            )
        )
        WebDriverWait(self.driver, 10).until(
                EC.title_is("Log in | Library"),
        )
        login_link = self.driver.find_element(By.LINK_TEXT, "Login")
        assert login_link.is_displayed()
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "message-error")
            )
        )
        assert error_message.is_displayed()

    def teardown_method(self):
        self.driver.quit()