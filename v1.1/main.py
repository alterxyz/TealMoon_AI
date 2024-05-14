"""
The telegram api has changed.
Normal commands may be working, but the message handler is not working.

`caused error MessageFilter.check_update() missing 1 required positional argument: 'update'`
"""

from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN: Final = config['TOKENtg']['v1']
BOT_USERNAME: Final = '@tealmoon_ai_v1_bot'

# Command Handlers


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am Tealmoon AI. How can I help you?')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'I am Tealmoon AI. \nI can help you with your daily tasks. Just ask me anything!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

# Message Handlers


def handle_response(text: str) -> str:
    processed: str = text.lower().strip()

    if 'hi' in processed:
        return 'Hello! How can I help you?'

    if 'goodbye' in processed:
        return 'Goodbye! Have a nice day!'

    return f'You said: /n{text}\n, but I am not sure how to respond to that.'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type} said: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(
        f'Update {update}\n\ncaused error {context.error}\n----------------------')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.Text, handle_message))

    # Error Handler
    app.add_error_handler(error)

    # Polling
    print('Bot is running!')
    app.run_polling(poll_interval=3)
