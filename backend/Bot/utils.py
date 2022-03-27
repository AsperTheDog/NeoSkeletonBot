import datetime

import disnake


def formatGuild(gld: disnake.Guild, carry):
    res = {
        'banner': gld.banner.url if gld.banner else "",
        'name': gld.name,
        'id': gld.id,
        'owner': gld.owner_id,
        'icon': gld.icon.url,
        'description': gld.description,
        'max_members': gld.max_members,
        'member_count': gld.member_count,
        'channels': {ch.id: ch.name for ch in gld.channels},
        'members': {}
    }
    for usr in gld.members:
        if usr.id not in carry:
            carry.append(usr.id)
        res['channels'][usr.id] = formatUser(usr, carry)

    return res


def formatUser(usr, carry, guild=None):
    res = {
        'id': usr.id,
        'avatar': usr.display_avatar.url,
        'bot': usr.bot,
        'banner': usr.banner.url if usr.banner else "",
        'created date': usr.created_at.timestamp(),
        'name': usr.name,
        'nick': usr.nick if guild else "",
        'discriminator': usr.discriminator,
        'identifier': usr.name + "#" + usr.discriminator,
        'roles': {role.id: role.name for count, role in enumerate(usr.roles)} if guild else {},
        'mention': usr.mention,
        'top_role': usr.top_role.id if guild else -1
    }
    if isinstance(usr, disnake.Member) and guild and usr.guild.id not in carry:
        carry.append(usr.guild.id)
        res['guild'] = formatGuild(usr.guild, carry)

    return res


def formatReactions(reacts: list[disnake.Reaction]):
    return {react.emoji: react.count for react in reacts}


def formatMessage(msg: disnake.Message, carry: list):
    res = {
        'id': msg.id,
        'content': msg.content,
        'channel': msg.channel.id,
        'datetime': msg.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
        'date': msg.created_at.strftime("%m/%d/%Y"),
        'time': msg.created_at.strftime("%H:%M:%S"),
        'timestamp': msg.created_at.timestamp(),
        'reactions': formatReactions(msg.reactions)
    }
    if msg.author.id not in carry:
        carry.append(msg.author.id)
        res['author'] = formatUser(msg.author, carry)
    if msg.guild.id not in carry:
        carry.append(msg.guild.id)
        res['guild'] = formatGuild(msg.guild, carry)
    return res


def sendError(message, trigger):
    emb = disnake.Embed(
        timestamp=datetime.datetime.now(),
        title="Error while executing a process",
        description=message,
        colour=disnake.Colour.red()
    )
    emb.set_footer(text=trigger)
    return emb
