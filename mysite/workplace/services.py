from datetime import timezone, timedelta, datetime
import time
import json
from workplace.models import Member
from workplace_login.workplace_login import WorkplaceLogin
from scrape_commute import ScrapeCommute
from crypto import Crypto
from create_logger import create_logger

crypto = Crypto()
logger = create_logger('services')


def members_login(email, password):
    member = get_member('email', email)
    workplace_login = WorkplaceLogin()
    login_res = workplace_login.login(crypto.decrypts(email),
                                      crypto.decrypts(password))
    if login_res != True:
        workplace_login.quit_firefox()
        raise Exception(login_res)
    cookie = workplace_login.get_cookies()
    workplace_login.quit_firefox()
    member.password = password
    member.cookie = crypto.encrypts_long(json.dumps(cookie))
    member.save()


def members_add(email, discord_id):
    remove_duplicate_members(email, discord_id)
    Member.objects.create(email=crypto.encrypts(email),
                          discord_id=crypto.encrypts(discord_id))
    return '등록 완료. https://workplace.cono.kr 로그인해주세요'


def remove_duplicate_members(email, discord_id):
    for field, value in [('email', email), ('discord_id', discord_id)]:
        try:
            member = get_member(field, value)
            member.delete()
        except Member.DoesNotExist:
            pass


def today():
    return datetime.fromtimestamp(time.time(), timezone(
        timedelta(hours=9))).strftime('%Y%m%d')


def validate(start_date, end_date):
    try:
        start_date = datetime.strptime(start_date,
                                       '%Y-%m-%d').strftime('%Y%m%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')
    except Exception:
        start_date = today()
        end_date = today()
    return start_date, end_date


def commute(discord_id, start_date, end_date):
    is_success = False
    data = False

    start_date, end_date = validate(start_date, end_date)
    member = get_member('discord_id', discord_id)

    if member.cookie:
        is_success, data = scrape_commute(member.cookie, start_date, end_date)

    if not is_success and member.password:
        members_login(member.email, member.password)
        member = get_member('discord_id', discord_id)
        is_success, data = scrape_commute(member.cookie, start_date, end_date)

    return is_success, data


def scrape_commute(cookie, start_date, end_date):
    is_success = False
    cookie = crypto.decrypts_long(cookie)
    scrape_commute = ScrapeCommute()
    scrape_commute.set_session(cookie)
    data = scrape_commute.send_api(start_date, end_date)

    if data:
        is_success = True

    return is_success, data


def is_encrypted(value):
    return len(value) > 100


def get_member(field, value):
    if is_encrypted(value):
        value = crypto.decrypts(value)

    encrypted_values = Member.objects.values_list(field, flat=True)

    for encrypted_value in encrypted_values:
        decrypted_value = crypto.decrypts(encrypted_value)
        if decrypted_value == value:
            return Member.objects.get(**{field: encrypted_value})

    raise Member.DoesNotExist(f'먼저, 계정을 등록해주세요.')
