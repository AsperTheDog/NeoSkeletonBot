import datetime

import disnake


def formatGuild(gld: disnake.Guild):
    return {
        'banner': gld.banner.url if gld.banner else "",
        'name': gld.name,
        'id': gld.id,
        'owner': gld.owner_id,
        'icon': gld.icon.url,
        'description': gld.description,
        'max members': gld.max_members,
        'member count': gld.member_count,
        'afk channel': gld.afk_channel.id if gld.afk_channel else -1
    }


def formatUser(usr: disnake.User):
    return {
        'id': usr.id,
        'avatar': usr.display_avatar.url,
        'bot': usr.bot,
        'banner': usr.banner.url if usr.banner else "",
        'created date': usr.created_at.timestamp,
        'name': usr.name,
        'discriminator': usr.discriminator,
        'identifier': usr.name + "#" + usr.discriminator,
        'mention': usr.mention
    }


def formatMember(usr):
    if isinstance(usr, disnake.User):
        return formatUser(usr)
    return {
        'id': usr.id,
        'avatar': usr.display_avatar.url,
        'bot': usr.bot,
        'banner': usr.banner.url if usr.banner else "",
        'created date': usr.created_at.timestamp,
        'activity': usr.activity.name if usr.activity else "",
        'name': usr.name,
        'nick': usr.nick if usr.nick else usr.name,
        'discriminator': usr.discriminator,
        'identifier': usr.name + "#" + usr.discriminator,
        'mention': usr.mention,
        'top role ID': usr.top_role.id
    }


def formatReactions(reacts):
    return {react.emoji.id: react.count for react in reacts}


def formatReaction(react):
    return {
        'emoji': formatEmoji(react.emoji),
        'count': react.count,
        'message ID': react.message.id
    }


def formatEmoji(emoji: disnake.Emoji | disnake.PartialEmoji | str):
    if isinstance(emoji, str):
        return {
            'name': emoji,
            'id': None
        }
    return {
        'name': emoji.name,
        'id': emoji.id
    }


def formatFullEmoji(emoji: disnake.Emoji):
    return {
        'id': emoji.id,
        'name': emoji.name,
        'animated': emoji.animated,
        'from twitch': emoji.managed,
        'created at': emoji.created_at,
        'url': emoji.url
    }


def formatMessage(msg: disnake.Message):
    return {
        'id': msg.id,
        'content': msg.content,
        'datetime': msg.created_at,
        'reactions': formatReactions(msg.reactions),
        'author ID': msg.author.id,
        'channel ID': msg.channel.id
    }


def formatChannel(channel: disnake.TextChannel):
    return {
        'id': channel.id,
        'created at': channel.created_at,
        'name': channel.name,
        'mention': channel.mention,
        'category ID': channel.category_id if channel.category_id else -1
    }


def formatThread(thread: disnake.Thread):
    return {
        'id': thread.id,
        'archived': thread.archived,
        'archive duration': thread.auto_archive_duration,
        'created at': thread.created_at,
        'locked': thread.locked,
        'mention': thread.mention,
        'category ID': thread.category_id,
        'owner ID': thread.owner_id,
        'parent ID': thread.parent_id if thread.parent_id else -1
    }


def formatCategory(category: disnake.CategoryChannel):
    return {
        'id': category.id,
        'name': category.name,
        'mention': category.mention
    }


def formatRole(role: disnake.Role):
    return {
        'id': role.id,
        'created at': role.created_at,
        'mention': role.mention,
        'name': role.name,
        'is admin': role.permissions.administrator
    }


def formatSticker(sticker: disnake.GuildSticker):
    return {
        'id': sticker.id,
        'name': sticker.name,
        'created at': sticker.created_at,
        'url': sticker.url,
        'unicode': sticker.emoji
    }


def formatVoiceState(vstate: disnake.VoiceState):
    return {
        'afk': vstate.afk,
        'channel ID': vstate.channel.id if vstate.channel else -1,
        'deaf': vstate.deaf,
        'mute': vstate.mute,
        'requested': vstate.requested_to_speak_at if vstate.requested_to_speak_at else False,
        'self deaf': vstate.self_deaf,
        'self mute': vstate.self_mute,
        'self stream': vstate.self_stream,
        'self video': vstate.self_video,
        'suppress': vstate.suppress
    }


def formatGuildEvent(event: disnake.GuildScheduledEvent):
    return {
        'channel ID': event.channel_id if event.channel_id else -1,
        'creator ID': event.creator_id,
        'description': event.description,
        'id': event.id,
        'name': event.name,
        'user count': event.user_count
    }


def formatStageInstance(stage: disnake.StageInstance):
    return {
        'channelID': stage.channel_id,
        'id': stage.id,
        'topic': stage.topic
    }


def formatInvite(invite: disnake.Invite):
    return {
        'id': invite.id,
        'created at': invite.created_at,
        'expires at': invite.expires_at,
        'max uses': invite.max_uses,
        'max age': invite.max_age,
        'temporary': invite.temporary,
        'uses': invite.uses,
        'creatorID': invite.inviter.id if invite.inviter else -1,
        'url': invite.url
    }


def sendError(message, trigger):
    emb = disnake.Embed(
        timestamp=datetime.datetime.now(),
        title="Error while executing a process",
        description=message,
        colour=disnake.Colour.red()
    )
    emb.set_footer(text=trigger)
    return emb
