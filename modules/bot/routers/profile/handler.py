from aiogram import Router
from aiogram import types

from modules.bot.keyboard_texts import MainKeyboardTexts

router = Router(name=__name__)

async def gen_reflink(botname,user_id):
    return f"https://t.me/{botname}?start={user_id}"

async def preapre_message(user,botname):
    user_id  = await user.user_id
    refs     = await user.get_referrals()
    reflink  = await(botname,user_id)    

    return (
        f"Ваш id: <b>{user_id}</b>\n"
        f"Приглашено: <b>{refs} чел.</b>\n\n"
        f"🔗 За каждого приглашенного друга ты получаешь 50₽ на баланс, друг получает 100₽.\n\n"
        f"👥 <b>Твоя реферальная ссылка:</b>\n{gen_reflink(botname,user_id)}\n"
    )



@router.dp.message(lambda message: message.text == MainKeyboardTexts.profile_text )
async def profile(message :types.Message):
        user_id  = message.chat.id
        user = await self.db_manager.get_user(user_id)
        #balance  = await user.get_balance(user_id)
        

        msg = self.texts.profile_text(refs,user_id,bot_username)
        keyboard = self.keyboards.profile_keyboard

        await message.reply(text = msg,
                            parse_mode=ParseMode.HTML,)
