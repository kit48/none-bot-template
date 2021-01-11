from nonebot import on_notice
from nonebot.rule import Rule
from nonebot.adapters.cqhttp import Bot, Event, GroupRecallNoticeEvent, FriendRecallNoticeEvent, Message
from nonebot.typing import T_State, Union
from nonebot.log import logger
from typing import Dict, Any


async def recall_checker(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupRecallNoticeEvent) or isinstance(event, FriendRecallNoticeEvent)


anti_recall = on_notice(rule=Rule(recall_checker), priority=10)


@anti_recall.handle()
async def handle_anti_recall(bot: Bot, event: Union[GroupRecallNoticeEvent, FriendRecallNoticeEvent], state: T_State):
    message_detail = await bot.get_msg(message_id=event.message_id)

    user_info = await get_user_info(message_detail, bot)
    user_text = ' '.join(user_info + ['撤回了：\n'])

    user_segment = {"type": "text", 'data': {'text': user_text}}
    message_segment = message_detail['message']

    logger.info(f'recall message detail: {message_segment}')

    for superuser in bot.config.superusers:
        await bot.send_private_msg(user_id=int(superuser), message=Message([user_segment] + message_segment))


async def get_user_info(message: Dict[str, Any], bot: Bot):
    user_id = message['sender']['user_id']
    nickname = message['sender']['nickname']
    group_id = message['group_id']
    if group_id:
        group_name = (await bot.get_group_info(group_id=group_id))['group_name']
        nickname_in_group = (await bot.get_group_member_info(group_id=group_id, user_id=user_id))['card']
        return [f'@{nickname_in_group}', f'#{group_name}']
    return [f'@{nickname}']
