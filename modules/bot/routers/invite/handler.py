import logging
import types

from aiogram import F, Router,Bot
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message, callback_query

from modules.bot.routers.invite import keyboard
from modules.bot.models import ServicesContainer
from modules.database.models import User
from modules.bot.utils.navigation import NavInvite, NavMain
from modules.utils.constants import PREVIOUS_CALLBACK_KEY
from modules.bot.filters import ReplyButtonFilter
from config import Config


from sqlalchemy.ext.asyncio import AsyncSession

from tools.image_container import ImageContainer

logger = logging.getLogger(__name__)
router = Router(name=__name__)

def gen_invite_link(bot_name:str,user:User):
    return f'https://t.me/{bot_name}?start={user.tg_id}'


async def prepare_message(config: Config,bot_name:str,user:User) ->str:
    invited_count               = user.referrals
    #rewarded                    = invited_count * config.shop.DAY_PRICE
    #reward_per_firend_balance   = config.shop.REFERRER_REWARD_PERIOD * config.shop.DAY_PRICE
    #reward_per_friend_days      = config.shop.REFERRER_REWARD_PERIOD
    #ivnited_reward_balance      = config.shop.REFERRED_TRIAL_PERIOD  * config.shop.DAY_PRICE
    #invited_reward_days         = config.shop.REFERRED_TRIAL_PERIOD
    invite_link                = gen_invite_link(bot_name,user)

    return _("invite:message:main").format(invite_link = invite_link,
                                           invited_count = invited_count) 


@router.callback_query(F.data == NavInvite.MAIN)
async def invite(   callback    : CallbackQuery,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession,
                    images : ImageContainer):
    logger.info(f"User {user.tg_id} opened invite page.")
    await state.update_data({PREVIOUS_CALLBACK_KEY: NavInvite.MAIN})
    bot_username = (await callback.bot.get_me()).username 
    text = await prepare_message(config,bot_username, user )
    markup = keyboard.invite_keyboard()
    result =  await callback.message.edit_media(media = InputMediaPhoto(media   = images.invite,
                                                                        caption = text)
                                                ,
                                                reply_markup=markup)
    return result

