from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import SearchStates
from database import requests
from utils import foundprofile_template
from keyboards.builders import choice_keyboard

router = Router()


@router.message(SearchStates.search_profile)
async def search_profile(message: Message, state: FSMContext):
    found_profile = await requests.find_profile(tg_id=message.from_user.id)
    if found_profile:
        await message.answer_photo(photo=found_profile.photo, caption=foundprofile_template(username=found_profile.username, age=found_profile.age,\
                                                                                            city=found_profile.city, description=found_profile.description, sex=found_profile.sex),\
                                                                                            reply_markup=choice_keyboard(['❤️', '👎', '💌'], size=(3, 1)))
        await state.set_state(SearchStates.rate_profile)
    