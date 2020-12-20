import json
import aiohttp
import nonebot
from nonebot.log import logger
from typing import Union, List

from .config import Config
from .typing import Image

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())


async def search_images(word: str) -> Union[List[Image], None]:
    logger.info(f'search images word: {word}')
    if not word:
        return None

    params = {
        "tn": "resultjson_com",
        "ipn": "rj",
        "is": "",
        "fp": "result",
        "queryWord": word,
        "ie": "utf-8",
        "oe": "utf-8",
        "ic": "0",
        "hd": "1",
        "word": word,
        "istype": "2",
        "nc": "1",
        "cg": "star",
        "pn": "30",
        "rn": "30",
    }

    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.get(plugin_config.SEARCH_API, params=params) as response:
                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None

                resp_payload = json.loads(await response.text())
                # logger.info(f'response: {resp_payload}')
                return resp_payload['data']
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return None
