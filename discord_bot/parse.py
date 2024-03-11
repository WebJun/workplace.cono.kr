from datetime import timedelta, datetime
from dotmap import DotMap  # pip install dotmap
from create_logger import create_logger

logger = create_logger('parse')


class Parse:

    day_of_week_korean = {
        'Monday': '월',
        'Tuesday': '화',
        'Wednesday': '수',
        'Thursday': '목',
        'Friday': '금',
        'Saturday': '토',
        'Sunday': '일'
    }

    def rest_message(self, data):
        print(data)
        # qqq = []
        # for commute in data.msg.data.list:
        #     if commute.dayTpCd == 'WORK':
        #         result = DotMap()
        #         result.date = self.extract_date(commute.checkYmd)
        #         result.real_in_hm = self.extract_time(commute.realInHm)
        #         result.real_out_hm = self.extract_time(commute.realOutHm)
        #         result.rest_time = self.extract_time(commute.restTime)
        #         qqq.append(result)
        work_day = self.work_day(data)
        print(work_day)
        total_work_time = self.total_work_time(data)
        print(total_work_time)
        # no_leave_office = self.no_leave_office(data)
        # rest = work_day * 8 - total_work_time / no_leave_office
        # current_time = 60
        # add_time = current_time + rest
        return '17시 30분(휴게시간 30분 기준)'

    def total_work_time(self, data):
        work_times = []
        time_format = '%H:%M'
        for commute in data.data.list:
            if commute.dayTpCd == 'WORK':
                start = self.extract_time(commute.realInHm)
                end = self.extract_time(commute.realOutHm)
                rest = self.extract_time(commute.restTime)
                
                start = datetime.strptime(start, time_format)
                end = datetime.strptime(end, time_format)
                hour = rest.split(':')[0]
                minute = rest.split(':')[1]
                rest = timedelta(hours=int(hour), minutes=int(minute))
                work_time = end - start - rest
                work_times.append(work_time)
        total_work_time = sum(work_times, timedelta())
        return total_work_time

    def work_day(self, data):
        result = 0
        for commute in data.data.list:
            if commute.dayTpCd == 'WORK':
                result = result + 1
        return result

    def run(self, data):
        qqq = []
        for commute in data.data.list:
            if commute.dayTpCd == 'WORK':
                result = DotMap()
                result.date = self.extract_date(commute.checkYmd)
                result.real_in_hm = self.extract_time(commute.realInHm)
                result.real_out_hm = self.extract_time(commute.realOutHm)
                result.rest_time = self.extract_time(commute.restTime)
                qqq.append(result)
        return qqq

    def extract_date(self, original):
        date_object = datetime.strptime(original, "%Y%m%d")
        date = date_object.strftime('%m/%d')
        day_of_week_english = date_object.strftime("%A")
        day = self.day_of_week_korean[day_of_week_english]
        return f'{date}({day})'

    def extract_time(self, original):
        if original is None:
            return None
        target_time = datetime.strptime(original, "%H%M")
        return target_time.strftime('%H:%M')

    def create_message(self, results):
        sss = []
        for result in results:
            date = result.date
            if result.real_in_hm:
                date = result.date
                if result.real_out_hm:
                    work_time = self.work_time(result.real_in_hm,
                                               result.real_out_hm,
                                               result.rest_time)
                    times = f'{result.real_in_hm}~{result.real_out_hm} / 근무({work_time}) / 휴게({result.rest_time})'
                else:
                    times = f'{result.real_in_hm}~...'
            else:
                times = '(없음)'
            sss.append(f'**{date}** {times}')
        return '\n'.join(sss)

    def work_time(self, real_in_hm, real_out_hm, rest_time):
        '''
        근무 시간을 구한다.
        real_in_hm 출근 시각
        real_out_hm 퇴근 시각
        rest_time 휴게 시간
        '''
        time_format = '%H:%M'
        real_in_time = datetime.strptime(real_in_hm, time_format)
        real_out_time = datetime.strptime(real_out_hm, time_format)
        rest_time_delta = timedelta(hours=int(rest_time.split(':')[0]),
                                    minutes=int(rest_time.split(':')[1]))
        elapse_time = real_out_time - real_in_time - rest_time_delta
        formatted_time = "{:01}시간 {:02}분".format(
            elapse_time.seconds // 3600, (elapse_time.seconds // 60) % 60)
        return formatted_time
