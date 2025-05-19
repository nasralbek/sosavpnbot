import logging

from aiogram import Router,types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile,Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.i18n import gettext as _

from sqlalchemy.ext.asyncio import AsyncSession

from modules.bot.utils.navigation import NavMain
from modules.utils.constants import MAIN_MESSAGE_ID_KEY
from modules.database.models import  User

from .texts import welcome_text
from .keyboard import main_keyboard 
from config import Config

logger = logging.getLogger(__name__)
class Handler():
    def __init__(self):
            #,bot
            self.router = Router(name=__name__)
            # self.app_manager = 'app_manager'
            # self.bot = bot
            self.sosa_vpn_banner = FSInputFile("./src/vpn_banner.jpg")
            self._register_handlers()


    async def register_user_notify(self,user_id,ref_id):
        await self.bot.send_message(user_id,
                                    "🎉 Вы зарегистрировались по реферальной ссылке! <b>Вам начислено 100₽.</b>",
                                    parse_mode=ParseMode.HTML)
        await self.bot.send_message(ref_id, 
                                    "🎉 Ваш друг зарегистрировался по реферальной ссылке! <b>Вам начислено 50₽.</b>",
                                    parse_mode=ParseMode.HTML)

    async def start(self,
                    message: types.Message,
                    user: User,
                    state: FSMContext,
                    config: Config,
                    session: AsyncSession,
                    command: CommandObject,
                    is_new_user: bool,
                    ):
        #TODO fix error when ref register multiple times
        #getting ids
        logger.info(f"User {user.tg_id} opened main menu page.")
        previous_message_id = await state.get_value(MAIN_MESSAGE_ID_KEY)
        if previous_message_id:
            try:
                await message.bot.delete_message(chat_id=user.tg_id, message_id=previous_message_id)
                logger.debug(f"Main message for user {user.tg_id} deleted.")
            except Exception as exception:
                logger.error(f"Failed to delete main message for user {user.tg_id}: {exception}")
            finally:
                await state.clear()

        received_referrer_id = int(command.args) if command.args and command.args.isdigit() else None
        if received_referrer_id and is_new_user:
            #TODO REFERRAL WORK THERE
            ref_id = message.text.split(" ")[1] if len(message.text.split()) > 1 else 0
            ref_id=int(ref_id)
            user_id = message.from_user.id
            print(f"{user_id} invited by {ref_id}")

        
        main_menu = await message.answer_photo(
                                    photo=self.sosa_vpn_banner,
                                    caption=_("main_menu:message:main").format(
                                        vpn_name        = config.bot.BOT_VPN_NAME,
                                        channel_tag     = config.bot.CHANNEL_TAG,
                                        chat_tag        = config.bot.CHAT_TAG,
                                        devices_count   = config.shop.DEVICES_COUNT 
                                    ),
                                    reply_markup=main_keyboard,
                                    parse_mode=ParseMode.HTML)
        
        await state.update_data({MAIN_MESSAGE_ID_KEY: main_menu.message_id})
        
        #check is user already exists
        # if await self.app_manager.is_user_exists(user_id):
        #     return
        
        # await self.app_manager.register_user(user_id)

        #register user
        # referral program
        # if ref_id:
        #     await self.register_user_notify(user_id,ref_id)
        #     await self.app_manager.new_referral(user_id,ref_id)

    def test_handler(message : Message,):
        logger.debug("test start handler")

    def _register_handlers(self):
        print("initializing start handler")
        self.router.message(
              Command(NavMain.MAIN)
        )(self.start)

