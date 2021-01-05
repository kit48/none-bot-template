import re
from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, Event, Message, exception
from nonebot.log import logger
from nonebot.exception import StopPropagation
from asyncstdlib.builtins import map as amap, list as alist

from .data_source import get_video_info, get_target_link

bili_cover = on_message(priority=10, block=False)

reg = re.compile(r'https://www.bilibili.com/video/[0-9a-zA-Z]+')
short_reg = re.compile(r'https://b23.tv/[0-9a-zA-Z]+')


@bili_cover.handle()
async def handle_image(bot: Bot, event: Event, state: dict):
    message = str(event.get_message())

    short_result = short_reg.findall(message)
    short_links = list(set(short_result))
    # https://stackoverflow.com/questions/62846735/how-to-use-await-inside-map-function
    makeup_links = await alist(amap(get_target_link, short_links))

    result = reg.findall(message + ' '.join(makeup_links))
    links = list(filter(lambda link: type(link) == str, list(set(result))))
    bvs = list(map(lambda link: link.split('/')[-1].replace('BV', ''), links))
    for bv in bvs:
        info = await get_video_info(bv)
        if info and 'url' in info:
            text = [
                # f'bv: {bv}',
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
            await bili_cover.send(f'未找到 bv {bv} 相关信息')
    if len(links):
        raise StopPropagation
