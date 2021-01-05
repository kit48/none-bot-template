import re
from nonebot import on_message
from nonebot.exception import StopPropagation
from nonebot.adapters.cqhttp import Bot, MessageEvent

echo = on_message(priority=20, block=False)

echo_maps = [
    {
        'reply': '确实。',
        'rules': [
            '不会',
            '应该',
            re.compile('.*YYDS.*', re.IGNORECASE),
            '我是',
            '我就是',
            '这就是',
            re.compile('.是.[^?？][?？]$')
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
            re.compile('flag', re.IGNORECASE),
        ]
    }
]


@echo.handle()
async def handle_indeed(bot: Bot, event: MessageEvent, state: dict):
    message = str(event.get_message())

    # print('user id', event.user_id)
    # print('message id', event.message_id)
    # print('bot config', bot.config)

    for echo_map in echo_maps:
        for rule in echo_map['rules']:
            if type(rule) is re.Pattern and rule.search(message):
                await echo.send(echo_map['reply'])
                raise StopPropagation()
            elif type(rule) is str and rule in message:
                await echo.send(echo_map['reply'])
                raise StopPropagation()
