from nonebot import on_notice
from nonebot.rule import Rule
from nonebot.adapters.cqhttp import Bot, Event, GroupRecallNoticeEvent, FriendRecallNoticeEvent, Message
from nonebot.typing import T_State, Union
from nonebot.log import logger


async def recall_checker(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupRecallNoticeEvent) or isinstance(event, FriendRecallNoticeEvent)


anti_recall = on_notice(rule=Rule(recall_checker), priority=10)


@anti_recall.handle()
async def handle_anti_recall(bot: Bot, event: Union[GroupRecallNoticeEvent, FriendRecallNoticeEvent], state: T_State):
    message_detail = await bot.get_msg(message_id=event.message_id)

    # user_id = message_detail['sender']['user_id']
    nickname = message_detail['sender']['nickname']
    group_id = message_detail['group_id']
    group_name = (await bot.get_group_info(group_id=group_id))['group_name'] if group_id else None
    at_group = f'#{group_name}' if group_name else None

    user_text = ' '.join(filter(lambda x: x, [f'@{nickname}', f'{at_group}', '撤回了：\n']))

    user_segment = {"type": "text", 'data': {'text': user_text}}
    message_segment = message_detail['message']

    logger.info(f'recall message detail: {message_segment}')

    for superuser in bot.config.superusers:
        await bot.send_private_msg(user_id=int(superuser), message=Message([user_segment] + message_segment))
