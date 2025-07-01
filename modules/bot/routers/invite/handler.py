import logging
import types

from aiogram import F, Router,Bot
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, callback_query

from modules.bot.routers.invite import keyboard
from modules.bot.services import ServicesContainer
from modules.database.models import User
from modules.bot.utils.navigation import NavInvite, NavMain
from modules.utils.constants import PREVIOUS_CALLBACK_KEY
from modules.bot.filters import ReplyButtonFilter
from config import Config


from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
router = Router(name=__name__)

def gen_invite_link(bot_name:str,user:User):
    return f'https://t.me/{bot_name}?start={user.tg_id}'


async def prepare_message(config: Config,bot_name:str,user:User) ->str:
    invited_count               = user.referrals
    rewarded                    = invited_count * config.shop.DAY_PRICE
    reward_per_firend_balance   = config.shop.REFERRER_REWARD_PERIOD * config.shop.DAY_PRICE
    reward_per_friend_days      = config.shop.REFERRER_REWARD_PERIOD
    ivnited_reward_balance      = config.shop.REFERRED_TRIAL_PERIOD  * config.shop.DAY_PRICE
    invited_reward_days         = config.shop.REFERRED_TRIAL_PERIOD
    referral_url                = gen_invite_link(bot_name,user)

    return _("invite_friend:message:main").format(  invited_count             = invited_count ,
                                                    reward_amount             = rewarded ,
                                                    reward_per_firend_balance = reward_per_firend_balance, 
                                                    reward_per_friend_days    = reward_per_friend_days ,
                                                    ivnited_reward_balance    = ivnited_reward_balance ,
                                                    invited_reward_days       = invited_reward_days ,
                                                    referral_url              = referral_url
)


@router.callback_query(F.data == NavInvite.MAIN)
async def invite(   callback    : CallbackQuery,
                    user        : User,
                    state       : FSMContext,
                    services    : ServicesContainer,
                    config      : Config,
                    session     : AsyncSession):
    logger.info(f"User {user.tg_id} opened invite page.")
    await state.update_data({PREVIOUS_CALLBACK_KEY: NavInvite.MAIN})
    bot_username = (await callback.bot.get_me()).username 
    text = await prepare_message(config,bot_username, user )
    markup = keyboard.invite_keyboard()
    result =  await callback.message.edit_text(text=text,
                                               reply_markup=markup)
    return result

