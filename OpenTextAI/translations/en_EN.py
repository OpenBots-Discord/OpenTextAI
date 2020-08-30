def on_join_message():
    return 'Thank you for choosing me. I am an open source OpenTextAI bot that can generate messages based on your chat messages.\
To get started, type in ai.help.'


def help_title():
    return 'List of commands'


def help_text():
    return '**Syntax: <...> - optional argument, 1|2|3 - conditional "or"**\n\
`ai.s|set` - set the current channel as the default chat (where messages will be indexed).\n\
`ai.g|gen|genetate <1|2|3>` - generate a random phrase, the length depends on the selected level: 1, 2 or 3; default is 2.\n\
`ai.b|burgut` - generate "burgut". You can learn more about them here: https://vk.com/bugurt_thread.\n\
`ai.d|dialog|dialogue` - generate a random dialogue.'


def gen_title():
    return 'Generated phrase'


def burgut_title():
    return 'Burgut'


def dialogue_title():
    return 'Generated dialogue:'


def set_chat_msg():
    return 'This chat has been successfully selected as the default chat. Now the recording of your previous messages has begun, this is necessary for the bot to learn better.\
During indexing, you cannot use the text generation commands, however, messages are usually recorded within a minute. After successful recording, I will notify about it myself.'


def reset_chat_msg():
    return 'The default chat was successfully reset.'


def successful_index():
    return 'The chat has been successfully indexed, now you can use the generating commands. Subsequent messages will be indexed automatically.\
Also, with a probability of 3 percent, the bot will write a randomly generated phrase in the chat.'


def missing_perms():
    return 'You do not have sufficient rights to execute this command.'


def missing_bot_perms():
    return 'I do not have sufficient rights to execute this command. Please grant all rights to the role that will allow this command to run.'


def too_late_gen():
    return 'Error: chat is still indexing.'
