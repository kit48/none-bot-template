import re
import json
from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, Event, Message, exception
from nonebot.log import logger
from nonebot.exception import StopPropagation
# from asyncstdlib.builtins import map as amap, list as alist
import aiohttp

from src.plugins.kit48.config import API_ROOT

bili_cover = on_message(priority=10, block=False)

reg = re.compile(r'https://www.bilibili.com/video/[0-9a-zA-Z]+')
short_reg = re.compile(r'https://b23.tv/[0-9a-zA-Z]+')


@bili_cover.handle()
async def handle_image(bot: Bot, event: Event, state: dict):
    message = str(event.get_message())

    short_result = short_reg.findall(message)
    short_links = list(set(short_result))
    # # https://stackoverflow.com/questions/62846735/how-to-use-await-inside-map-function
    # makeup_links = await alist(amap(get_target_link, short_links))

    result = reg.findall(message)
    links = list(filter(lambda link: type(link) == str, list(set(result)))) + short_links
    for link in links:
        info = await get_data(link)
        if info and 'url' in info:
            text = [
                f"{link}",
                f"UP: {info['up']}",
                f"标题: {info['title']}"
            ]
            if info['desc']:
                text.append(f"简介：{info['desc']}")
            message = Message([
                {
                    "type": "image",
                    "data": {"file": info['url']}
                }, {
                    "type": "text",
                    "data": {
                        "text": '\n'.join(text)
                    }
                }])
            await bili_cover.send(message)
        else:
            await bili_cover.send(f'未找到 {link} 相关信息')
    if len(links):
        raise StopPropagation


async def get_data(url: str):
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(f"{API_ROOT}/bilibili/covers", params={"url": url}) as response:
                if response.status != 200:
                    return None

                return json.loads(await response.text())
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as err:
        logger.error(err)
        return None
