import json
from datetime import datetime
import requests  # pip install requests
from create_logger import create_logger
import pytz
from config.config import env

logger = create_logger('scrape_commute')


class ScrapeCommute:

    session = None

    # date는 20240120 이런 형태
    def send_api(self, start_date, end_date):
        response_text = ''
        try:
            headers = {
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            }
            params = {
                'fromDate': start_date,
                'toDate': end_date,
                'empId': env('EMP_ID'),
                'chkWorkingDay': 'N',
                '_': self.timestamp()
            }
            response = self.session.get(
                'https://cowave.ncpworkplace.com/user/commute-status/list',
                params=params,
                headers=headers,
            )
            response_text = response.text
            return response.json()
        except Exception as exception:
            logger.exception(exception)
            logger.error(response_text)
            return False

    def timestamp(self):
        korea_timezone = pytz.timezone('Asia/Seoul')  # 한국 시간대 설정
        current_time = datetime.now(korea_timezone)  # 현재 한국 시간을 가져옴
        return int(current_time.timestamp() * 1000)  # 초를 밀리초로 변환

    def set_session(self, cookies_str):
        try:
            cookies_list = json.loads(cookies_str)
            session = requests.Session()
            for cookie in cookies_list:
                session.cookies.set(cookie['name'], cookie['value'])
            self.session = session
        except:
            print('set_session error')
