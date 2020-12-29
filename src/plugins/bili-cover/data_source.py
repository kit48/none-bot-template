import json
import aiohttp
from nonebot.log import logger
from typing import Union

from .typing import VideoInfo


async def get_target_link(short_link: str) -> str:
    if not short_link:
        return None
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(short_link) as response:
                if response.status != 200:
                    return None
                return str(response.url)
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as err:
        logger.error(err)
        return None


async def get_video_info(bv: str) -> Union[VideoInfo, None]:
    if not bv:
        return None

    params = {
        "type": "bv",
        "id": bv,
        "clien": "2.2.0"
    }

    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get("https://api.magecorn.com/bilicover/get-cover.php", params=params, headers={
                "referer": "https://bilicover.magecorn.com/"
            }) as response:
                if response.status != 200:
                    return None

                text = await response.text()
                # json.loads 限制太多，反括号前有逗号都会报错
                processed_text = text.replace('\n', '').replace('\r', '').replace(' ', '').replace(',}', '}')
                return json.loads(processed_text, strict=False)
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as err:
        logger.error(err)
        return None
