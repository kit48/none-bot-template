import json
import aiohttp
import nonebot
# import os
from nonebot.log import logger
from typing import Union, List

from .config import Config
from .typing import Image

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())


async def find_images(word: str) -> Union[List[Image], None]:
    logger.info(f'search images word: {word}')
    if not word:
        return None

    params = {
        # tn 字段说明：http://bitjoy.net/2015/08/13/baidu-image-downloader-python3-pyqt5-eric6-cx_freeze4/
        "tn": "resultjson",
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

                text = await response.text()
                # json.loads 限制太多，反括号前有逗号都会报错
                processed_text = text.replace('\n', '').replace('\r', '').replace(' ', '').replace(',}', '}')
                # with open(f'{os.getcwd()}/text.txt', 'w', encoding='utf-8') as f:
                #     f.write(json.dumps(json.loads(processed_text, strict=False), indent=2))
                resp_payload = json.loads(processed_text, strict=False)
                # print('images resp_payload', resp_payload)
                return resp_payload['data'] if resp_payload['displayNum'] > 0 else None
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as err:
        logger.error(err)
        # 抛出上面任何异常，说明调用失败
        return None
