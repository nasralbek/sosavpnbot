from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram import F
from remnawave_api.models import NodesResponseDto
from remnawave_api import RemnawaveSDK
from remnawave_api.models.nodes import NodeResponseDto

from services.admin.bot.navigation import NavMain

from .keyboard import admin_keyboard


router: Router = Router()


@router.message(Command("start"))
async def start(m: Message):
    await m.reply("this is admin bot",reply_markup=admin_keyboard())


def form_node_status(nodestatus):
    result = ""
    format = "<blockquote><b>%s: </b>%s</blockquote>\n"

    return format % ("NODE ID",nodestatus.uuid) + "\n"
    for key,value in dump.items():
        try:
            result += format % (key,value)
        except Exception as e:
            result += format % (key,str(e))
    return result+"\n\n"




@router.callback_query(F.data == NavMain.NODE_STATUS)
async def node_status(callback_query: CallbackQuery,
                      r_sdk : RemnawaveSDK):
    result = "NODE STATUS\n\n"

    nodes = await r_sdk.nodes.get_all_nodes()
    if not isinstance(nodes,NodesResponseDto):
        return await callback_query.message.answer("error getting nodes")
    for node in nodes.response:
        result += form_node_status(node)


        
    await callback_query.message.answer(result)
