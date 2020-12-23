import random
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment, exception
from nonebot.log import logger

from .data_source import find_images

image = on_command(cmd="img", aliases={"搜图"}, priority=10)


@image.handle()
async def handle_image(bot: Bot, event: Event, state: dict):
    message = str(event.message)

    images = await find_images(message)
    # TODO 使用抛出异常的方式统一处理，避免使用独立的异常处理逻辑
    if type(images) is list and len(images):
        logger.info(f'[{message}] images count: {len(images)}')
        reply_image = random.choice(images)
        # 使用 objURL 时，图片可能会不存在，不知道百度搜图这个操作啥意思 _(:3J∠)_
        obj_url = reply_image['objURL']
        middle_url = reply_image['middleURL']
        try:
            logger.info(f'reply obj_url: {obj_url}')
            # await image.finish(f'[CQ:image,file={escape(reply_image)}]') # 通过字符串暂时无法发送带有特殊符号的图片链接
            await image.finish(MessageSegment(type="image", data={"file": obj_url}))
        except exception.ActionFailed:
            logger.warning(f'reply obj_url failed, replaced by middle_url: {middle_url}')
            await image.finish(MessageSegment(type="image", data={"file": middle_url}))
    else:
        logger.info(f'[{message}] no images')
        await image.finish(f'未找到 [{message}] 相关图片 _(:3J∠)_')
