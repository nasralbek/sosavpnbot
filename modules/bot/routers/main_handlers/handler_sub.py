from aiogram import Router
from aiogram import types
from aiogram import Bot, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import ChatMember
from aiogram.enums import ChatMemberStatus
from .keyboard import invite_keyboard, connect_vpn_keyboard, information_keyboard

from modules.bot.utils.navigation import NavMain
from .texts import profile_text, connect_text, information_text


class Handler():
    def __init__(self, app_manager, bot_username):
        self.router = Router(name=__name__)
        self.bot_username = bot_username
        self.app_manager = app_manager
        self.CHANNEL_ID = -1002545855062

        self._register_handlers()
        self._register_callbacks()

    def _register_callbacks(self):
        self.router.callback_query(
            F.data == "check_subscription_connect"
        )(self._handle_subscription_check)
        
        self.router.callback_query(
            F.data == "check_subscription_information"
        )(self._handle_subscription_check_information)
        
        self.router.callback_query(
            F.data == "check_subscription_invite"
        )(self._handle_subscription_check_invite)

    async def is_user_subscribed(self, user_id: int, bot: Bot) -> bool:
        try:
            member = await bot.get_chat_member(chat_id=self.CHANNEL_ID, user_id=user_id)
            return member.status in [
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR
            ]
        except Exception as e:
            print(f"ERROR checking subscription: {e}")
            return False

    async def _handle_subscription_check(self, callback: types.CallbackQuery, bot: Bot):
        if await self.is_user_subscribed(callback.from_user.id, bot):
            await callback.message.delete()
            
            user = await self.app_manager.get_user(callback.from_user.id)
            key = await user.get_key()
            expiry_time = user.expiry_time
            msg = connect_text(key, expiry_time, user)
            keyboard = connect_vpn_keyboard().get()
            
            await callback.message.answer(text=msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        else:
            await callback.answer("❌ Ну ты врушка!", show_alert=True)

    async def _handle_subscription_check_information(self, callback: types.CallbackQuery, bot: Bot):
        if await self.is_user_subscribed(callback.from_user.id, bot):
            await callback.message.delete()
            msg = information_text
            keyboard = information_keyboard().get()
            await callback.message.answer(text=msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        else:
            await callback.answer("❌ Ну ты врушка!", show_alert=True)

    async def _handle_subscription_check_invite(self, callback: types.CallbackQuery, bot: Bot):
        if await self.is_user_subscribed(callback.from_user.id, bot):
            await callback.message.delete()
            user_id = callback.from_user.id
            user = await self.app_manager.get_user(user_id)
            msg = profile_text(user, self.bot_username)
            await callback.message.answer(text=msg, parse_mode=ParseMode.HTML)
        else:
            await callback.answer("❌ Ну ты врушка!", show_alert=True)

    async def invite_friend(self, message: types.Message, bot: Bot):
        user_id = message.from_user.id
        is_subscribed = await self.is_user_subscribed(user_id, bot)

        if not is_subscribed:
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="Подписаться", 
                    url="https://t.me/sosavpn"
                )],
                [types.InlineKeyboardButton(
                    text="Я подписался", 
                    callback_data="check_subscription_invite"
                )]
            ])
            await message.answer(
                "⚡️ Для продолжения работы с ботом <b>необходимо подписаться на наш новостной канал.</b> Там будут <b>только самые важные объявления.</b>",
                reply_markup=keyboard, parse_mode='html'
            )
            return

        user = await self.app_manager.get_user(user_id)
        msg = profile_text(user, self.bot_username)
        await message.answer(text=msg, parse_mode=ParseMode.HTML)

    async def information(self, message: types.Message, bot: Bot):
        user_id = message.from_user.id
        is_subscribed = await self.is_user_subscribed(user_id, bot)

        if not is_subscribed:
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="Подписаться", 
                    url="https://t.me/sosavpn"
                )],
                [types.InlineKeyboardButton(
                    text="Я подписался", 
                    callback_data="check_subscription_information"
                )]
            ])
            await message.answer(
                "⚡️ Для продолжения работы с ботом <b>необходимо подписаться на наш новостной канал.</b> Там будут <b>только самые важные объявления.</b>",
                reply_markup=keyboard, parse_mode='html'
            )
            return

        msg = information_text
        keyboard = information_keyboard().get()
        await message.answer(text=msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    async def connect(self, message: types.Message, bot: Bot):
        user_id = message.from_user.id
        is_subscribed = await self.is_user_subscribed(user_id, bot)

        if not is_subscribed:
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(
                    text="Подписаться", 
                    url="https://t.me/sosavpn"
                )],
                [types.InlineKeyboardButton(
                    text="Я подписался", 
                    callback_data="check_subscription_connect"
                )]
            ])
            await message.answer(
                "⚡️ Для продолжения работы с ботом <b>необходимо подписаться на наш новостной канал.</b> Там будут <b>только самые важные объявления.</b>",
                reply_markup=keyboard, parse_mode='html'
            )
            return

        user = await self.app_manager.get_user(user_id)
        key = await user.get_key()
        expiry_time = user.expiry_time
        msg = connect_text(key, expiry_time, user)
        keyboard = connect_vpn_keyboard().get()
        
        await message.answer(text=msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    def _register_handlers(self):
        print("initializing invite")
        self.router.message(
            lambda message: message.text == NavMain.INVITE
        )(self.invite_friend)

        print("initializing connect")
        self.router.message(
            lambda message: message.text == NavMain.CONNECT
        )(self.connect)

        print("initializing information")
        self.router.message(
            lambda message: message.text == NavMain.INFORMATION
        )(self.information)

        print("initializing invite,connect,information successfull")