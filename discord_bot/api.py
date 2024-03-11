import json
import urllib.parse
from dotmap import DotMap  # pip install dotmap
import aiohttp  # pip install aiohttp
from create_logger import create_logger

logger = create_logger('api')


class Api:

    base_url = 'https://workplace.cono.kr'
    user_id = None

    async def make_request(self, method, url, data=None):
        try:
            full_url = f'{self.base_url}{url}'
            async with aiohttp.ClientSession() as session:
                async with getattr(session, method)(full_url,
                                                    data=data) as response:
                    if response.status // 100 != 2:
                        raise aiohttp.ClientResponseError(
                            status=response.status, message='200대 아님')

                    result_data = DotMap(await response.json())
                    return result_data
        except aiohttp.ClientResponseError as e:
            logger.exception('서버 꺼져 있음')
            logger.exception(e)
            return False
        except Exception as e:
            logger.exception(e)
            return False

    async def get_commute(self, start_date, end_date):
        query_params = {
            'discord_id': self.user_id,
            'start_date': start_date,
            'end_date': end_date
        }
        url = f'/api/commute?{urllib.parse.urlencode(query_params)}'
        return await self.make_request('get', url)

    async def add_account(self, email, discord_account_id):
        data = {'email': email, 'discord_account_id': discord_account_id}
        url = '/api/members'
        return await self.make_request('post', url, data=json.dumps(data))
