import json
import aiohttp
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, escape, GroupMessageEvent
from nonebot.log import logger

from src.plugins.kit48.config import API_ROOT

tickets = on_command(cmd="tkt", aliases={"票务"}, priority=20)

group_map = {
    "上海": 1,
    "北京": 2,
    "广州": 3,
}


@tickets.handle()
async def handle_tuling(bot: Bot, event: Event, state: dict):
    message = str(event.get_message())

    group_id = get_group_id(message)

    data = await get_data(group_id)
    if data and len(data):
        await tickets.finish(escape('\n---\n'.join(map(format_ticket, data))))
    else:
        await tickets.reject('票务查询失败')


def get_group_id(message: str):
    for name, gid in group_map.items():
        if message.find(name) >= 0:
            return gid
    return group_map['上海']


def format_ticket(info):
    special = info['special'].replace('限定实名认证', '').strip()
    base_info = f'{info["addtime"]}\n{info["theme"]} {info["teamname"].upper()}'
    return f'{base_info}\n{special}' if special else base_info


async def get_data(gid: int):
    params = {
        "gid": gid,
    }

    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(f"{API_ROOT}/snh48g/tickets", params=params) as response:
                if response.status != 200:
                    return None

                return json.loads(await response.text())
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as err:
        logger.error(err)
        return None
