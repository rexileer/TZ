from aiogram import Router, types, F
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from keyboards.faq_kb import get_faq_keyboard
from services.faq_service import get_answer_from_db, search_faq_from_db

router = Router()


@router.message(F.text == "FAQ")
async def show_categories(message: Message):
    keyboard = await get_faq_keyboard()

    await message.answer("Выберите вопрос:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("faq_"))
async def handle_faq_answer(callback_query: types.CallbackQuery):
    faq_id = int(callback_query.data.split("_")[1])
    faq = await get_answer_from_db(faq_id)
    if faq:
        await callback_query.message.answer(f"{faq.question}\n\n{faq.answer}")
    else:
        await callback_query.message.answer("Ответ на этот вопрос не найден.")
    
    await callback_query.answer()

@router.message(F.text.startswith("@q"))
async def handle_search_query(message: Message):
    search_text = message.text[2:].strip()
    
    if search_text:
        faq_entries = await search_faq_from_db(search_text)
        
        if faq_entries:
            results = "\n\n".join([f"{faq.question}: {faq.answer}" for faq in faq_entries])
            await message.answer(results)
        else:
            await message.answer("Не удалось найти ответы на ваш запрос.")
    else:
        await message.answer("Пожалуйста, введите запрос после @q.")

@router.inline_query()
async def inline_search_faq(query: InlineQuery):
    search_text = query.query.strip()
    
    if search_text.startswith("@q"):
        search_text = search_text[2:].strip()
        
        if search_text:
            faq_entries = await search_faq_from_db(search_text)
            
            results = [
                InlineQueryResultArticle(
                    id=str(faq.id),
                    title=faq.question, 
                    input_message_content=InputTextMessageContent(faq.answer) 
                )
                for faq in faq_entries
            ]
            
            if not results:
                results.append(
                    InlineQueryResultArticle(
                        id="no_results",
                        title="Нет результатов",
                        input_message_content=InputTextMessageContent("По вашему запросу ничего не найдено.")
                    )
                )
            
            await query.answer(results, cache_time=60)
