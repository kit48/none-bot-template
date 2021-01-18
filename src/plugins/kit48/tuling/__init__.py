import random
import json
import aiohttp
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, escape, GroupMessageEvent
from nonebot.log import logger
from typing import Sequence, Union

from src.plugins.kit48.config import API_ROOT

tuling = on_message(rule=to_me(), priority=999)


def render_expression(expr,
                      *args,
                      escape_args: bool = True,
                      **kwargs) -> str:
    """
    Render an expression to message string.
    :param expr: expression to render
    :param escape_args: should escape arguments or not
    :param args: positional arguments used in str.format()
    :param kwargs: keyword arguments used in str.format()
    :return: the rendered message
    """
    result: str
    if callable(expr):
        result = expr(*args, **kwargs)
    elif isinstance(expr, Sequence) and not isinstance(expr, str):
        result = random.choice(expr)
    else:
        result = expr
    if escape_args:
        return result.format(
            *[escape(s) if isinstance(s, str) else s for s in args], **{
                k: escape(v) if isinstance(v, str) else v
                for k, v in kwargs.items()
            })
    return result.format(*args, **kwargs)


# 定义无法获取图灵回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)


@tuling.handle()
async def handle_tuling(bot: Bot, event: Event, state: dict):
    message = str(event.get_message())

    reply = await get_data(message, event.get_user_id(),
                           event.group_id if isinstance(event, GroupMessageEvent) else None)
    if reply:
        await tuling.finish(escape(reply))
    else:
        # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取图灵回复时的「表达」
        # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
        await tuling.reject(render_expression(EXPR_DONT_UNDERSTAND))


async def get_data(message: str, user_id: str, group_id: Union[str, None]):
    params = {
        "message": message,
        "userId": user_id,
    }

    if group_id:
        params['groupId'] = group_id

    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(f"{API_ROOT}/tuling", params=params) as response:
                if response.status != 200:
                    return None

                return await response.text()
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as err:
        logger.error(err)
        return None
