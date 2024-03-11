import discord  # pip install py-cord
from create_logger import create_logger
from config import env
from services import Services
import os

logger = create_logger('main')
logger.info(f'서버 시작 pid:{os.getpid()}')
bot = discord.Bot()

bot.description = 'WorkPlace에서 출퇴근을 가져옵니다.'


@bot.command(name='출근계정등록',
             description='출근 계정 등록합니다. 이메일, discord account id가 필요합니다.')
async def add_account(ctx, email, discord_account_id):
    try:
        services = Services()
        res = await services.add_account(email, discord_account_id)
        await ctx.respond(res)
    except Exception as e:
        await ctx.send(str(e))
        logger.exception(e)


@bot.command(name='출근', description='출퇴근 현황을 봅니다.')
async def get_commute_info(ctx):
    try:
        user_id = ctx.author.id
        services = Services()
        res = await services.get_commute_info(ctx, user_id)
        await ctx.send(res)
    except Exception as e:
        await ctx.send(str(e))
        logger.exception(e)


@bot.command(name='퇴근시각', description='퇴근시각을 알려줍니다.(주40시간)')
async def get_leave_office_time(ctx):
    try:
        user_id = ctx.author.id
        services = Services()
        res = await services.get_leave_office_time(user_id)
        await ctx.respond(res)
    except Exception as e:
        await ctx.send(str(e))
        logger.exception(e)


bot.run(env('BOT_TOKEN'))
