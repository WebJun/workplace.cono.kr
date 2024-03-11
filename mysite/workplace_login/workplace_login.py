from func_timeout import func_set_timeout  # pip install func-timeout
from create_logger import create_logger
from workplace_login import seleniums

logger = create_logger('workplace_login')


class WorkplaceLogin:

    seleniums = None

    def __init__(self):
        self.seleniums = seleniums.Seleniums()

    @func_set_timeout(60)
    def login(self, email, password):
        try:
            if not self.seleniums.wait_login_page():
                raise Exception('wait_login_page')
            if not self.seleniums.login_inner(email, password):
                raise Exception('login_inner')
            # 순차적으로 하지 말고,
            # TODO::메인페이지 이동과 에러 메시지 둘 중 먼저 나오는걸로 해야함.
            if not self.seleniums.wait_main_page():
                raise Exception('wait_main_page')
            return True
        except Exception as err:
            logger.error(err)
            if 'wait_main_page' in str(err):
                return self.seleniums.extract_error_message()
            return False

    def get_cookies(self):
        return self.seleniums.get_cookies()

    def quit_firefox(self):
        if self.seleniums:
            self.seleniums.quit_firefox()
            self.seleniums = None
