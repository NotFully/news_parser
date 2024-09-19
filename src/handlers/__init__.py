import asyncio
import aiogram
from aiogram import Bot
from secrets import choice
from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.types import URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import URLInputFile
from aiogram.fsm.state import StatesGroup, State


from kb.keyboard import kb_menu
from kb.inline import my_channels, under_channel, get_my_keyword_under_channel, get_under_keyboard_kb
from utils.db.keywords import Keyword

from kb.keyboard import kb_menu
from kb.inline import my_channels, under_channel_for_my_channels
from utils.db.my_channels import Channel