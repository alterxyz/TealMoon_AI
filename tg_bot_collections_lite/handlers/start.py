from os import environ
import time
import datetime

from telebot import TeleBot
from telebot.types import Message
from expiringdict import ExpiringDict

from . import *

import cohere
from telegramify_markdown import convert
from telegramify_markdown.customize import markdown_symbol


def start_handler(message: Message, bot: TeleBot) -> None:
    """start : /start"""
    who = "Hi"
    reply_id = bot_reply_first(message, who, bot)
    s = f"Ask me anything! Try starting your question by /models with your following words,\nor simply copy and paste this word into your message👉: `/cohere Is Toronto still hot as last year?`\nExplore more options by clicking the **Menu**."
    bot_reply_markdown(reply_id, who, s, bot, split_text=False)


def register(bot: TeleBot) -> None:
    bot.register_message_handler(start_handler, commands=["start"], pass_bot=True)
