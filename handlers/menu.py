from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import GlobalStates, SearchStates
from handlers.commands import send_profile

router = Router()


@router.message(GlobalStates.menu)
async def menu_choices(message: Message, state: FSMContext):
    if message.text == '👤 Моя анкета':
        await send_profile(message=message, state=state)
    elif message.text == '🚀 Искать анкеты':
        await state.set_state(SearchStates.search_profile)
    elif message.text == '❤️ Кто меня оценил?':
        await message.answer('Вас лайкнули:')
    else:
        await message.answer('Нет такого варианта ответа')
