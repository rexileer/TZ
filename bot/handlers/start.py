from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards import reply, catalog

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer( "Welcome to the AnyTechShop bot! Please choose an action from the menu.", reply_markup=reply.main)
    
#change the code below - Command("catalog")
@router.message(Command("catalog"))
async def show_categories(message: Message):
    keyboard = await catalog.get_categories_keyboard(page=1)
    await message.answer("-------Choose a category-------", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("page_"))
async def paginate_categories(callback_query: CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    keyboard = await catalog.get_categories_keyboard(page=page)
    
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()
