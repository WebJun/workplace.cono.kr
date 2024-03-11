from api import Api
from create_logger import create_logger
import asyncio
from datetime import timedelta, datetime
from parse import Parse

logger = create_logger('services')
api = Api()
parse = Parse()


class Services:

    async def add_account(self, email, discord_account_id):
        try:
            res = await api.add_account(email, discord_account_id)
            return res
        except Exception as e:
            logger.exception(e)
            return False

    async def get_commute_info(self, ctx, user_id):
        task1 = asyncio.create_task(self.async_waiting(ctx))
        task2 = asyncio.create_task(self.async_data(user_id))
        # asyncio.gather를 사용하여 두 작업을 동시에 실행
        done, pending = await asyncio.wait([task1, task2],
                                           return_when=asyncio.FIRST_COMPLETED)

        # 첫 번째 완료된 작업 이외의 작업들을 취소
        for task in pending:
            task.cancel()

        # 결과를 확인하기 위해 asyncio.gather를 재사용
        results = await asyncio.gather(*done)

        # task2.result는 results 리스트에서 직접 사용할 수 있습니다.
        return results[0]

    async def get_leave_office_time(self, user_id):
        '''
        남은시간 = 
        일주일에 WORK인 날 곱하기 8
        - worktime의 총합
        - 연차인 시간

        WORK인데 퇴근 안찍은날로 나누기
        그다음에 그 시간을 오늘 출근시간에 더하고 휴게시간 더해서 리턴한다
        17시 30분(휴게시간 30분 기준)
        '''
        api.user_id = user_id
        start_date, end_date = self.this_week_period()
        data = await api.get_commute(start_date, end_date)
        if not data.is_success:
            raise Exception(data.message)
        return parse.rest_message(data.data)

    async def async_waiting(self, ctx):
        await ctx.respond('데이터 가져오는 중')
        await asyncio.sleep(1)
        message = await ctx.send('데이터 가져오는 중')
        for num in range(1, 30):
            dots = '.' * num
            await asyncio.sleep(1)
            await message.edit(content=f'데이터 가져오는 중{dots}')

    async def async_data(self, user_id):
        api.user_id = user_id
        start_date, end_date = self.this_week_period()
        data = await api.get_commute(start_date, end_date)

        if not data.is_success:
            raise Exception('data.is_success ERROR')

        result = parse.run(data.data)
        message = parse.create_message(result)
        return message

    # 월요일이 시작일
    def this_week_period(self):
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_date = start_of_week.strftime("%Y-%m-%d")
        end_date = end_of_week.strftime("%Y-%m-%d")
        return start_date, end_date
