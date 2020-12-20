import random
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, escape
from nonebot.log import logger

from .data_source import search_images

image = on_command(cmd="img", aliases={"搜图"}, rule=to_me(), priority=10)


@image.handle()
async def handle_image(bot: Bot, event: Event, state: dict):
    message = str(event.message)

    images = await search_images(message)
    reply_image = random.choice(images)["middleURL"]
    logger.info(f'reply image: {reply_image}')
    logger.info(f'reply message: [CQ:image,file={escape(reply_image)}]')
    if reply_image:
        await image.finish(f'[CQ:image,file={escape(reply_image)}]')
    else:
        await image.reject('failed')
