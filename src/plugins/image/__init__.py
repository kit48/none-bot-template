import random
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, Message, exception
from nonebot.log import logger

from .data_source import find_images

image = on_command(cmd="img", aliases={"搜图"}, priority=10)


def get_message(event: Event, url: str):
    at_segment = {"type": "at", "data": {"qq": event.user_id}}
    image_segment = {"type": "image", "data": {"file": url}}

    if event.detail_type == 'group':
        return Message([image_segment, at_segment])
    return Message(image_segment)


@image.handle()
async def handle_image(bot: Bot, event: Event, state: dict):
    message = str(event.message)

    images = await find_images(message)
    # TODO 使用抛出异常的方式统一处理，避免使用独立的异常处理逻辑
    if type(images) is list and len(images):
        logger.info(f'[{message}] images count: {len(images)}')
        reply_image = random.choice(images)
        # logger.info(f'reply_image: {reply_image}')
        # 使用 objURL 时，图片可能会不存在，不知道百度搜图这个操作啥意思 _(:3J∠)_
        # 可能是由于百度会从源地址去下载原图，但是原图不存在的问题
        obj_url = reply_image['objURL']
        middle_url = reply_image['middleURL']
        logger.info(f'obj_url: {obj_url}')
        logger.info(f'middle_url: {middle_url}')
        try:
            # await image.finish(f'[CQ:image,file={escape(reply_image)}]') # 通过字符串暂时无法发送带有特殊符号的图片链接
            await image.finish(get_message(event, obj_url))
            logger.info(f'reply obj_url: {obj_url}')
        except exception.ActionFailed:
            logger.warning(f'reply obj_url failed, retry by middle_url')
            await image.finish(get_message(event, middle_url))
    else:
        logger.info(f'[{message}] no images')
        await image.finish(f'未找到 [{message}] 相关图片 _(:3J∠)_')
