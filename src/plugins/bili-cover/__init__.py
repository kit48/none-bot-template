import re
from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, Event, Message, exception
from nonebot.log import logger

from .data_source import get_video_info

bili_cover = on_message(priority=10)

reg = re.compile(r'https://www.bilibili.com/video/[0-9a-zA-Z]+')


@bili_cover.handle()
async def handle_image(bot: Bot, event: Event, state: dict):
    message = str(event.message)

    result = reg.findall(message)
    for item in list(set(result)):
        bv = item.split('/')[-1].replace('BV', '')
        info = await get_video_info(bv)
        if info and 'url' in info:
            message = Message([
                {
                    "type": "image",
                    "data": {"file": info['url']}
                }, {
                    "type": "text",
                    "data": {
                        "text": f"bv: {bv}\ntitle: {info['title']}\ndesc: {info['desc']}"
                    }
                }])
            await bili_cover.send(message)
        else:
            await bili_cover.send(f'未找到 bv {bv} 相关信息')
