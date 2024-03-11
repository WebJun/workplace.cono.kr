from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from workplace_login.browser_factory import BrowserFactory
from create_logger import create_logger

logger = create_logger('seleniums')


class Seleniums:

    timeout = 3
    bs = None

    def __init__(self):
        bf = BrowserFactory()
        self.bs = bf.create('firefox')
        self.bs.get('https://cowave.ncpworkplace.com/')

    def wait_login_page(self):
        try:
            WebDriverWait(self.bs, self.timeout).until(
                EC.presence_of_element_located((By.ID, 'user')))
            return True
        except TimeoutException as e:
            logger.error(f'wait_login_page 타임아웃: {str(e)}')
            return False

    def login_inner(self, email, password):
        try:
            email_input = self.bs.find_element(By.ID, 'user')
            email_input.send_keys(email)

            password_input = self.bs.find_element(By.ID, 'password')
            password_input.send_keys(password)

            login_button = self.bs.find_element(By.ID, 'loginBtn')
            login_button.click()

            return True
        except NoSuchElementException as e:
            logger.error('login_inner 에러: 요소를 찾을 수 없음')
            return False
        except Exception as e:
            logger.error(f'login_inner 에러: {str(e)}')
            return False

    def wait_main_page(self):
        try:
            WebDriverWait(self.bs, self.timeout).until(
                EC.presence_of_element_located((By.ID, 'workplaceLayer')))
            return True
        except TimeoutException as e:
            logger.error('wait_main_page 타임아웃')
            return False

    def extract_error_message(self):
        try:
            fail_message_element = self.bs.find_element(
                By.ID, 'div_fail_message')
            return fail_message_element.text
        except NoSuchElementException as e:
            return ''

    def get_cookies(self):
        return self.bs.get_cookies()

    def quit_firefox(self):
        self.bs.quit()
