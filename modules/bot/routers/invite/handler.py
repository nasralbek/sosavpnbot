import logging

from aiogram import F, Router,Bot
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from modules.bot.services import ServicesContainer
from modules.database.models import User
from modules.bot.utils.navigation import NavMain
from modules.utils.constants import PREVIOUS_CALLBACK_KEY
from modules.bot.filters import ReplyButtonFilter
from config import Config


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


async def invite(  message : Message,
                        user:User,
                        state:FSMContext,
                        config: Config,
                        bot : Bot):
    logger.info(f"User {user.tg_id} opened connect page.")
    await state.update_data({PREVIOUS_CALLBACK_KEY: NavMain.INVITE})
    client_data = None
    logger.debug(state)

    text = await prepare_message(config,(await bot.get_me()).username ,user )

    result =  await message.answer(text = text,)
    return result

@router.message(ReplyButtonFilter("main_menu:button:invite_friend"))
async def information_message(
    message : Message,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config,
    bot : Bot
):return await invite(message,user,state, config,bot)

@router.callback_query(F.data == NavMain.INVITE)
async def information_callback(
    callback: CallbackQuery,
    user: User,
    services: ServicesContainer,
    state: FSMContext,
    config: Config,
    bot : Bot
):return await invite(callback.message,user,state,config,bot)
