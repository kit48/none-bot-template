import re
from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, escape
from typing import Sequence

echo = on_message(priority=20)

echo_maps = [
    {
        'reply': '确实。',
        'rules': [
            '不会',
            '应该',
            'YYDS',
            '我是',
            '我就是',
            '这就是',
            re.compile('.[^?？][?？]$')
        ]
    },
    {
        'reply': '羡慕',
        'rules': [
            'XM',
            '羡慕'
        ]
    },
    {
        'reply': '我信了',
        'rules': [
            'flag',
        ]
    }
]


@echo.handle()
async def handle_indeed(bot: Bot, event: Event, state: dict):
    message = str(event.message)

    for echo_map in echo_maps:
        for rule in echo_map['rules']:
            if type(rule) is re.Pattern and rule.search(message):
                await echo.finish(echo_map['reply'])
                return
            elif type(rule) is str and rule in message:
                await echo.finish(echo_map['reply'])
                return
