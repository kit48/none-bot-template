import re
from nonebot import on_message
from nonebot.exception import StopPropagation
from nonebot.adapters.cqhttp import Bot, MessageEvent

echo = on_message(priority=20, block=False)

REPEAT = 'repeat'

echo_maps = [
    {
        'reply': '确实。',
        'rules': [
            '不会真',
            '应该',
            '我是',
            '我就是',
            '这就是',
            re.compile('.是.[^?？][?？]$')
        ]
    },
    {
        'reply': REPEAT,
        'rules': [
            re.compile('.*XM.*', re.IGNORECASE),
            re.compile('.*羡慕.*'),
            re.compile('.*YYDS.*', re.IGNORECASE),
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
async def handle_echo(bot: Bot, event: MessageEvent, state: dict):
    message = str(event.get_message())

    # print('user id', event.user_id)
    # print('message id', event.message_id)
    # print('bot config', bot.config)

    for echo_map in echo_maps:
        for rule in echo_map['rules']:
            if type(rule) is re.Pattern and rule.search(message):
                await send_message(echo_map['reply'], message)
                raise StopPropagation()
            elif type(rule) is str and rule in message:
                await send_message(echo_map['reply'], message)
                raise StopPropagation()


async def send_message(reply: str, message: str):
    if reply == REPEAT:
        await echo.send(message)
    else:
        await echo.send(reply)
