from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import utils
import keyboards as kb
import validators
from states import Register

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=utils.welcome_greet(message.from_user.first_name), reply_markup=kb.register_button)


@router.callback_query(F.data == 'signup')
async def start_reg(callback: CallbackQuery, state=FSMContext):
    await callback.answer('')
    await state.set_state(Register.sex)
    await callback.message.answer('Введите ваш пол', reply_markup=kb.sex_choice)


@router.message(Register.sex)
async def handle_sex(message: Message, state: FSMContext):
    if validators.sex_validate(message.text):
        if message.text == 'Мужской':
            await state.update_data(sex=0)
        else:
            await state.update_data(sex=1)

        await state.set_state(Register.search_desire)
        await message.answer('Чьи анкеты вы хотитите смотреть?', reply_markup=kb.search_desire)
        return
    await message.answer('Введите пол корректно', reply_markup=kb.sex_choice)
    return


@router.message(Register.search_desire)
async def handle_search_desire(message: Message, state: FSMContext):
    if validators.search_desire_validate(message.text):
        if message.text == 'Парней':
            await state.update_data(search_desire=0)
        elif message.text == 'Девушек':
            await state.update_data(search_desire=1)
        else:
            await state.update_data(search_desire=2)
        
        await state.set_state(Register.name)
        await message.answer('Введите ваше имя')
        return
    await message.answer('Выберите корректно.\nЧьи анкеты вы хотитите смотреть?', reply_markup=kb.search_desire)
    return


@router.message(Register.name)
async def handle_name(message: Message, state: FSMContext):
    if validators.name_validate(message.text):
        await state.update_data(name=message.text)
        await state.set_state(Register.age)
        await message.answer('Введите ваш возраст')
        return 
    await message.answer('Введите имя корректно (до 20 символов)')
    return


@router.message(Register.age)
async def handle_age(message: Message, state: FSMContext):
    if validators.age_validate(message.text):
        await state.update_data(age=int(message.text))
        await state.set_state(Register.city)
        await message.answer('Введите ваш город')
        return
    await message.answer('Введите возраст корректно')
    return 


@router.message(Register.city)
async def handle_city(message: Message, state: FSMContext):
    if validators.city_validate(message.text):
        await state.update_data(city=message.text)
        await state.set_state(Register.description)
        await message.answer('Напишите описание для своей анкеты')
        return
    await message.answer('Введите город корректно')
    return


@router.message(Register.description)
async def handle_description(message: Message, state: FSMContext):
    if validators.description_validate(message.text):
        await state.update_data(description=message.text)
        await state.set_state(Register.photo)
        await message.answer('Отправьте фото для вашей анкеты')
        return
    await message.answer('Введите описание корректно')
    return


@router.message(Register.photo)
async def handle_photo(message: Message, state: FSMContext):
    if validators.photo_validate(message.photo):
        await state.update_data(photo=message.photo[-1].file_id)
        await send_profile(message=message, state=state)
        return
    await message.answer('Отправьте фото корректно')
    return


async def send_profile(message: Message, state: FSMContext):
    profile_data = await state.get_data()
    await message.answer('Регистрация завершена. Вот ваша анкета: ')
    await message.answer_photo(photo=profile_data['photo'], \
                                caption=f'{profile_data['name']}, {profile_data['age']}, {profile_data['city']}, {profile_data['description']}')
    