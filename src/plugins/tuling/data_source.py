import json
import aiohttp
import nonebot
import hashlib
from nonebot.adapters.cqhttp import Event
from nonebot.log import logger
from typing import Optional

from .config import Config

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())


def context_id(event: Event, *, mode: str = 'default',
               use_hash: bool = False) -> str:
    """
    Calculate a unique id representing the context of the given event.
    mode:
      default: one id for one context
      group: one id for one group or discuss
      user: one id for one user
    :param event: the event object
    :param mode: unique id mode: "default", "group", or "user"
    :param use_hash: use md5 to hash the id or not
    """
    ctx_id = ''
    if mode == 'default':
        if event.group_id:
            ctx_id = f'/group/{event.group_id}'
        if event.user_id:
            ctx_id += f'/user/{event.user_id}'
    elif mode == 'group':
        if event.group_id:
            ctx_id = f'/group/{event.group_id}'
        elif event.user_id:
            ctx_id = f'/user/{event.user_id}'
    elif mode == 'user':
        if event.user_id:
            ctx_id = f'/user/{event.user_id}'

    if ctx_id and use_hash:
        ctx_id = hashlib.md5(ctx_id.encode('ascii')).hexdigest()
    return ctx_id


async def call_tuling_api(event: Event, text: str) -> Optional[str]:
    logger.info(f'input text: {text}')
    if not text:
        return None

    # 构造请求数据
    payload = {
        'reqType': 0,
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': plugin_config.API_KEY,
            'userId': context_id(event, use_hash=True)
        }
    }

    group_unique_id = context_id(event, mode='group', use_hash=True)
    if group_unique_id:
        payload['userInfo']['groupId'] = group_unique_id

    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.post(plugin_config.API_URL, json=payload) as response:
                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None

                resp_payload = json.loads(await response.text())
                logger.info(f'response: {resp_payload}')
                if resp_payload['results']:
                    for result in resp_payload['results']:
                        if result['resultType'] == 'text':
                            # 返回文本类型的回复
                            return result['values']['text']
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return None
