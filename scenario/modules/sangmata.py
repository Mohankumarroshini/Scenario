# Copyright (C) 2021 ElizaRobot
# made by @Eliza_Robot on Telegram. 
# github account : https://github.com/kira-36/
# This file is part of ElizaRobot (Telegram Bot)

import datetime 
import asyncio
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types

from scenario.events import register
from scenario import telethn
from scenario import ubot


async def is_register_admin(chat, user):

    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
 
        return isinstance(
            (
                await telethn(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await telethn.get_peer_id(user)
        ps = (
            await telethn(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


@register(pattern="^/sg ?(.*)")
async def _(event):

    if event.fwd_from:

        return

    if event.is_group:
        if await is_register_admin(event.input_chat, event.message.sender_id):
            pass
        else:
            return
    if not event.reply_to_msg_id:

        await event.reply("```Reply to any user message.```")

        return

    reply_message = await event.get_reply_message()

    if not reply_message.text:

        await event.reply("```reply to text message```")

        return

    chat = "Sangmatainfo_bot"
    uid = reply_message.sender_id
    reply_message.sender

    if reply_message.sender.bot:

        await event.edit("```Reply to actual users message.```")

        return

    lol = await event.reply("```Processing```")

    async with ubot.conversation(chat) as conv:

        try:

            # response = conv.wait_event(
            #   events.NewMessage(incoming=True, from_users=1706537835)
            # )

            await silently_send_message(conv, f"/search_id {uid}")

            # response = await response
            responses = await silently_send_message(conv, f"/search_id {uid}")
        except YouBlockedUserError:

            await event.reply("```Please unblock @Sangmatainfo_bot and try again```")

            return
        await lol.edit(f"{responses.text}")
        # await lol.edit(f"{response.message.message}")

__help__ = """
  • /sg*:* Get A Name History Of User
          
          🥺 This module is not fully optimised. Suggest your commans in @Mastro_Support
"""

__mod_name__ = "sᴀɴɢᴍᴀᴛᴀ✨"
