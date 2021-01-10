from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.log import logger

# 展示所有接收到的信息，比如方便测试 QQ 表情等特殊消息的数据结构
print_plugin = on_message(priority=1, block=False)


@print_plugin.handle()
async def handle_print(bot: Bot, event: MessageEvent, state: dict):
    message = str(event.get_message())
    logger.info(f'receive message: {message}')
