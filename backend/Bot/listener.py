import json
from datetime import datetime

import disnake
from disnake.ext import commands

from fsmLogic.boardManager import BoardManager
from Bot import utils


class EventListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author == self.bot.user:
            return
        BoardManager.sendGlobalEvent(self.bot, "on message received", utils.formatMessage(message), message.guild)

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        BoardManager.sendGlobalEvent(self.bot, "on message deleted", utils.formatMessage(message), message.guild)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        data = {
            'before': utils.formatMessage(before),
            "after": utils.formatMessage(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on message edited", data, after.guild)

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        data = {
            'channel': channel.id,
            'user': utils.formatMember(user),
            'when': when if when else datetime.now().timestamp()
        }
        BoardManager.sendGlobalEvent(self.bot, "on typing", data, channel.guild)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        data = {
            'reaction': utils.formatReaction(reaction),
            'user': utils.formatMember(user)
        }
        BoardManager.sendGlobalEvent(self.bot, "on reaction added", data, reaction.message.guild)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        data = {
            'reaction': utils.formatReaction(reaction),
            'user': utils.formatMember(user)
        }
        BoardManager.sendGlobalEvent(self.bot, "on reaction removed", data, reaction.message.guild)

    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        data = {
            'reactions': utils.formatReactions(reactions),
            'message': utils.formatMessage(message)
        }
        BoardManager.sendGlobalEvent(self.bot, "on reaction cleared", data, message.guild)

    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, reaction):
        BoardManager.sendGlobalEvent(self.bot, "on reaction emoji cleared", utils.formatReaction(reaction), reaction.message.guild)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        BoardManager.sendGlobalEvent(self.bot, "on channel created", utils.formatChannel(channel), channel.guild)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        BoardManager.sendGlobalEvent(self.bot, "on channel deleted", utils.formatChannel(channel), channel.guild)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        data = {
            'before': utils.formatChannel(before),
            "after": utils.formatChannel(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on channel edited", data, after.guild)

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        BoardManager.sendGlobalEvent(self.bot, "on channel pins updated", utils.formatChannel(channel), channel.guild)

    @commands.Cog.listener()
    async def on_thread_join(self, thread):
        BoardManager.sendGlobalEvent(self.bot, "on thread joined", utils.formatThread(thread), thread.guild)

    @commands.Cog.listener()
    async def on_thread_remove(self, thread):
        BoardManager.sendGlobalEvent(self.bot, "on thread removed", utils.formatThread(thread), thread.guild)

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        BoardManager.sendGlobalEvent(self.bot, "on thread deleted", utils.formatThread(thread), thread.guild)

    @commands.Cog.listener()
    async def on_thread_member_join(self, member):
        user = self.bot.get_guild(member.thread.guild.id).get_member(member.id)
        data = {
            'thread': utils.formatThread(member.thread),
            'user': utils.formatMember(user)
        }
        BoardManager.sendGlobalEvent(self.bot, "on member joined thread", data, member.thread.guild)

    @commands.Cog.listener()
    async def on_thread_member_remove(self, member):
        user = self.bot.get_guild(member.thread.guild.id).get_member(member.id)
        data = {
            'thread': utils.formatThread(member.thread),
            'user': utils.formatMember(user)
        }
        BoardManager.sendGlobalEvent(self.bot, "on member left thread", data, member.thread.guild)

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        data = {
            'before': utils.formatThread(before),
            "after": utils.formatThread(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on thread updated", data, after.guild)

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        BoardManager.sendGlobalEvent(self.bot, "on webhooks updated", utils.formatChannel(channel), channel.guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        BoardManager.sendGlobalEvent(self.bot, "on member joined", utils.formatMember(member), member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        BoardManager.sendGlobalEvent(self.bot, "on member left", utils.formatMember(member), member.guild)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        data = {
            'before': utils.formatMember(before),
            "after": utils.formatMember(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on member updated server profile", data, after.guild)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        data = {
            'before': utils.formatUser(before),
            "after": utils.formatUser(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on user updated profile", data, after.guild)

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        data = {
            'before': utils.formatMember(before),
            "after": utils.formatMember(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on member presence updated", data, after.guild)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        BoardManager.sendGlobalEvent(self.bot, "on role created", utils.formatRole(role), role.guild)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        BoardManager.sendGlobalEvent(self.bot, "on role removed", utils.formatRole(role), role.guild)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        data = {
            'before': utils.formatRole(before),
            "after": utils.formatRole(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on role updated", data, after.guild)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        data = {
            'before': utils.formatGuild(before),
            "after": utils.formatGuild(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on guild updated", data, after.guild)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        data = {
            'before': utils.formatFullEmoji(before),
            "after": utils.formatFullEmoji(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on emoji updated", data, after.guild)

    @commands.Cog.listener()
    async def on_guild_stickers_update(self, guild, before, after):
        data = {
            'before': utils.formatSticker(before),
            "after": utils.formatSticker(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on sticker updated", data, after.guild)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        data = {
            'member': utils.formatMember(member),
            'before': utils.formatVoiceState(before),
            "after": utils.formatVoiceState(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on member voice updated", data, after.guild)

    @commands.Cog.listener()
    async def on_guild_scheduled_event_create(self, event):
        BoardManager.sendGlobalEvent(self.bot, "on event created", utils.formatGuildEvent(event), event.guild)

    @commands.Cog.listener()
    async def on_guild_scheduled_event_delete(self, event):
        BoardManager.sendGlobalEvent(self.bot, "on event created", utils.formatGuildEvent(event), event.guild)

    @commands.Cog.listener()
    async def on_guild_scheduled_event_update(self, before, after):
        data = {
            'before': utils.formatGuildEvent(before),
            "after": utils.formatGuildEvent(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on event updated", data, after.guild)

    @commands.Cog.listener()
    async def on_guild_scheduled_event_subscribe(self, event, user):
        data = {
            'user': utils.formatMember(user),
            'event': utils.formatGuildEvent(event)
        }
        BoardManager.sendGlobalEvent(self.bot, "on event subscribed", data, event.guild)

    @commands.Cog.listener()
    async def on_guild_scheduled_event_unsubscribe(self, event, user):
        data = {
            'user': utils.formatMember(user),
            'event': utils.formatGuildEvent(event)
        }
        BoardManager.sendGlobalEvent(self.bot, "on event unsubscribed", data, event.guild)

    @commands.Cog.listener()
    async def on_stage_instance_create(self, stage):
        BoardManager.sendGlobalEvent(self.bot, "on stage instance created", utils.formatStageInstance(stage), stage.guild)

    @commands.Cog.listener()
    async def on_stage_instance_delete(self, stage):
        BoardManager.sendGlobalEvent(self.bot, "on stage instance deleted", utils.formatStageInstance(stage), stage.guild)

    @commands.Cog.listener()
    async def on_stage_instance_update(self, before, after):
        data = {
            'before': utils.formatStageInstance(before),
            "after": utils.formatStageInstance(after)
        }
        BoardManager.sendGlobalEvent(self.bot, "on stage instance updated", data, after.guild)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        BoardManager.sendGlobalEvent(self.bot, "on member banned", utils.formatMember(user), guild)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        BoardManager.sendGlobalEvent(self.bot, "on member unbanned", utils.formatMember(user), guild)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        BoardManager.sendGlobalEvent(self.bot, "on invite created", utils.formatInvite(invite), invite.guild)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        BoardManager.sendGlobalEvent(self.bot, "on invite deleted", utils.formatInvite(invite), invite.guild)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("fsmLogic/dataFiles/tracking/botGuilds.json", "w") as file:
            json.dump([guild.id for guild in self.bot.guilds], file)

# TODO: scheduled
