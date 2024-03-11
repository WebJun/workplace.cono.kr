from django.http import JsonResponse
from workplace import services
from dotmap import DotMap  # pip install dotmap
import json
from create_logger import create_logger
from django.views.decorators.csrf import csrf_exempt

logger = create_logger('views_back')


def members_login(request):
    result = default_result()
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        services.members_login(email, password)
        result.is_success = True
        return JsonResponse(result.toDict(), status=200)
    except Exception as e:
        result.message = str(e)
        logger.exception(e)
    return JsonResponse(result.toDict(), status=200)


@csrf_exempt
def members_add(request):
    result = default_result()
    try:
        if request.method != 'POST':
            raise Exception('Only POST requests are allowed.')
        data = json.loads(request.body)
        email = data.get('email')
        discord_id = data.get('discord_account_id')
        services.members_add(email, discord_id)
        result.is_success = True
        return JsonResponse(result.toDict(), status=200)
    except Exception as e:
        result.message = str(e)
        logger.exception(e)
    return JsonResponse(result.toDict(), status=200)


def commute(request):
    result = default_result()
    result.message = 'https://workplace.cono.kr 에 로그인해주세요.'
    try:
        discord_id = request.GET.get('discord_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        result.is_success, result.data = services.commute(discord_id, start_date, end_date)
        return JsonResponse(result.toDict(), status=200)
    except Exception as e:
        result.message = str(e)
        logger.exception(e)
    return JsonResponse(result.toDict(), status=200)


def default_result():
    default_result = DotMap()
    default_result.is_success = False
    default_result.data = {}
    default_result.message = '실패했습니다.'
    default_result.code = '500'
    return default_result
