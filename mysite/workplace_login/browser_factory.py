from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver_manager
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import SessionNotCreatedException
from config.config import env
from create_logger import create_logger
import os

logger = create_logger('browser_factory')


class BrowserFactory:

    def create(self, name='firefox'):
        try:
            if name == 'chrome':
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                return webdriver.Chrome(service=ChromeService(
                    ChromeDriverManager().install()),
                                        options=options)
            else:
                options = webdriver.FirefoxOptions()
                options.add_argument('--headless')
                options.set_preference('intl.accept_languages', 'ko-KR')
                driverPath = self.get_gecko_driver_path()
                return webdriver.Firefox(service=FirefoxService(driverPath),
                                         options=options)
        except SessionNotCreatedException:
            logger.error('브라우저를 설치하세요')

    def get_gecko_driver_path(self):
        res = env('GECKO_DRIVER_PATH')
        if os.path.isfile(res):
            return res
        return GeckoDriverManager().install()
