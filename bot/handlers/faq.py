from aiogram import Router, types, F
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from keyboards.faq_kb import get_faq_keyboard
from services.faq_service import get_answer_from_db

router = Router()


@router.message(F.text == "FAQ")
async def show_categories(message: Message):
    keyboard = await get_faq_keyboard()

    await message.answer("Выберите вопрос:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("faq_"))
async def handle_faq_answer(callback_query: types.CallbackQuery):
    faq_id = int(callback_query.data.split("_")[1])
    faq = await get_answer_from_db(faq_id)
    if faq:
        await callback_query.message.answer(f"{faq.question}\n\n{faq.answer}")
    else:
        await callback_query.message.answer("Ответ на этот вопрос не найден.")
    
    await callback_query.answer()

