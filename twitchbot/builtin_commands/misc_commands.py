from twitchbot import (
    channels,
    Command,
    commands,
    CommandContext,
    Message, get_all_custom_commands,
    cfg,
)


@Command('list')
async def cmd_list(msg: Message, *args):
    for c in channels.values():
        await msg.reply(
            whisper=True,
            msg=f'channel: {c.name}, viewers: {c.chatters.viewer_count}, is_mod: {c.is_mod}, is_live: {c.live}')


@Command('commands', context=CommandContext.BOTH, help='lists all commands')
async def cmd_commands(msg: Message, *args):
    custom_commands_str = ', '.join(cmd.name for cmd in get_all_custom_commands(msg.channel_name))
    global_commands_str = ', '.join(cmd.fullname for cmd in commands.values())

    await msg.reply(whisper=True, msg=f'GLOBAL: {global_commands_str}')

    if custom_commands_str:
        await msg.reply(whisper=True, msg=f'CUSTOM: {custom_commands_str}')


@Command(name='help', syntax='<command>', help='gets the help text for a command')
async def cmd_help(msg: Message, *args):
    if not args:
        await msg.reply(whisper=False, msg=f'syntax for {cfg.prefix}help: <command>')
        return

    cmd = commands.get(args[0]) or commands.get(cfg.prefix + args[0])
    if not cmd:
        await msg.reply(f'command not found, did you forget the prefix?')
        return

    await msg.reply(whisper=False, msg=f'help for {cmd.fullname} - syntax: {cmd.syntax} - help: {cmd.help}')


# testing command, uncomment @Command to enable
# @Command('mention')
async def cmd_mention(msg: Message, *args):
    print(msg.channel.chatters.all_viewers)
    await msg.reply(f'found mentions: {msg.mentions}')
