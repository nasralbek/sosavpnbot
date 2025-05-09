from aiogram import Router,types,F
from aiogram.filters import Command


from modules.bot.utils.navigation import NavConnect,NavPurshareMethod,NavDaysCount,NavConfirm

from .texts import topup_text,days_selected_text,method_selected_text
from .keyboard import topup_keyboard,select_method_keyboard,method_selected_keyboard,confirmed_keyboard


class Handler():
    def __init__(self,app_manager):
        self.router = Router(name=__name__)
        self.app_manager = app_manager

        self._register_handlers()

    async def topup(self,callback: types.CallbackQuery):
        text = topup_text
        keyboard = topup_keyboard()

        await callback.message.edit_text(text=text,reply_markup=keyboard)
        await callback.answer()

    async def days_selected(self,query,callback_data:NavPurshareMethod ):
        days    = callback_data.days
        price   = callback_data.price
        text = days_selected_text(days,price)
        keyboard = select_method_keyboard(days,price)

        await query.message.edit_text(text=text,reply_markup=keyboard)
         
    async def method_selected(self,query,callback_data: NavPurshareMethod):
        days        = callback_data.days
        price       = callback_data.price
        method      = callback_data.method

        text        = method_selected_text(days,price,method)
        keyboard    = method_selected_keyboard(days,price,method)
        await query.message.edit_text(text=text,reply_markup = keyboard)

    async def purshare_confirmed(self,query: types.CallbackQuery,callback_data: NavConfirm):
        days        = callback_data.days
        price       = callback_data.price
        method      = callback_data.method
        user_id = query.from_user.id

        text        = query.message.text
        url = await self.app_manager.create_transaction(user_id,price,days)
        keyboard    = confirmed_keyboard(url)

        await query.message.edit_text(text=text,reply_markup = keyboard)


    def _register_handlers(self):
        print("initializing top up handler")

        self.router.callback_query(
            lambda callback: callback.data == NavConnect.TOPUP
        )(self.topup)

        self.router.callback_query(
            NavDaysCount.filter()
        )(self.days_selected)

        self.router.callback_query(
            NavPurshareMethod.filter()
        )(self.method_selected)

        self.router.callback_query(NavConfirm.filter())(self.purshare_confirmed)



