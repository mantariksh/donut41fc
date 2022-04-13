import logging
import os
import random

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

updater = Updater(token=os.getenv('TELEGRAM_TOKEN'))
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# Hardcode names.
# Alternatives considered:
# 1. Write a command for people to add their names to the list,
# and store the names in a database. But a lot of dev effort and
# user effort to join as well.
# 2. Convert all relevant users to admins in the channel and use
# telegram API to get list of admins (telegram only offers an API
# to get the admins in a channel, not the full list of members).
# But a lot of manual work to convert one by one.
names = ['User ' + str(i) for i in range(40)]


def chunk(l, size=2, combine_remainder=True):
    if len(l) < size:
        return [l]
    if combine_remainder:
        chunks = []
        for i in range(0, len(l), size):
            toAppend = l[i:i+size]
            if len(toAppend) == size:
                chunks.append(toAppend)
            else:
                chunks[-1].extend(toAppend)
        return chunks
    else:
        return [l[i:i+size] for i in range(0, len(l), size)]


def generateGroupStrings(l, size=2, combine_remainder=True):
    random.shuffle(l)
    groups = chunk(l, size, combine_remainder)
    return ['\n'.join(g) for g in groups]


def assign(update: Update, context: CallbackContext):
    groupedList = generateGroupStrings(names, 3)
    textToSend = 'Here are your donut assignments! \U0001F369\n\n'
    textToSend += '\n\n'.join(groupedList)
    context.bot.send_message(chat_id=update.effective_chat.id, text=textToSend)


assign_handler = CommandHandler('assign', assign)
dispatcher.add_handler(assign_handler)

updater.start_polling()
