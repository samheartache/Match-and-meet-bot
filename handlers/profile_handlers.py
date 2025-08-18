from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import validators
import messages
import keyboards.replies as kb_r
from keyboards.builders import choice_keyboard
from states import Register
from utils import profile_template

router = Router()


@router.callback_query(F.data == 'signup')
async def start_signup(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(Register.sex)
    await state.update_data(tg_id=callback.message.from_user.id)
    await callback.message.answer(text='Введите ваш пол', reply_markup=choice_keyboard(['Мужской', 'Женский'], size=(2, 1)))


@router.message(Register.sex)
async def handle_sex(message: Message, state: FSMContext):
    if validators.sex_validate(data=message.text):
        sex = 1 if message.text == 'Мужской' else 0
        await state.update_data(sex=sex)
        await state.set_state(Register.search_desire)
        await message.answer(text='Чьи анкеты вы хотите смотреть?', reply_markup=kb_r.search_desire)
        return
    else:
        await message.answer(text='Выберите пол корректно', reply_markup=choice_keyboard(['Мужской', 'Женский'], size=(2, 1)))
        return


@router.message(Register.search_desire)
async def handle_search_desire(message: Message, state: FSMContext):
    if validators.search_desire_validate(message.text):
        search_desire = {'Парней': 1, 'Девушек': 0, 'Не важно': None}.get(message.text)
        await state.update_data(search_desire=search_desire)
        await state.set_state(Register.searched_by)
        await message.answer(text='Кому отображать вашу анкету?', reply_markup=kb_r.searched_by)
    else:
        await message.answer('Выберите корретно', reply_markup=kb_r.search_desire)
        return 


@router.message(Register.searched_by)
async def handle_searched_by(message: Message, state: FSMContext):
    if validators.searched_by_validate(message.text):
        searched_by = {'Девушкам': 0, 'Парням': 1, 'Не важно': None}.get(message.text)
        await state.update_data(searched_by=searched_by)
        await state.set_state(Register.name)
        await message.answer(text='Введите ваше имя', reply_markup=choice_keyboard(f'{message.from_user.username}'))
    else:
        await message.answer('Выберите корретно', reply_markup=kb_r.search_desire)
        return 


@router.message(Register.name)
async def handle_name(message: Message, state: FSMContext):
    if validators.name_validate(message.text):
        await state.update_data(username=message.text)
        await state.set_state(Register.age)
        await message.answer('Введите ваш возраст')
    else:
        await message.answer('Введите имя корректно', reply_markup=choice_keyboard(f'{message.from_user.username}'))
        return


@router.message(Register.age)
async def handle_age(message: Message, state: FSMContext):
    if validators.age_validate(message.text):
        await state.update_data(age=int(message.text))
        await state.set_state(Register.city)
        await message.answer('Введите город')
    else:
        await message.answer('Введите возраст корректно')
        return


@router.message(Register.city)
async def handle_city(message: Message, state: FSMContext):
    if validators.city_validate(message.text):
        await state.update_data(city=message.text)
        await state.set_state(Register.description)
        await message.answer('Отправьте описание для своего профиля', reply_markup=choice_keyboard('❌ Не указывать'))
    else:
        await message.answer('Введите город корректно')
        return


@router.message(Register.description)
async def handle_description(message: Message, state: FSMContext):
    if validators.description_validate(message.text):
        if message.text == '❌ Не указывать':
            await state.update_data(description=None)
        else:
            await state.update_data(description=message.text)
        await state.set_state(Register.photo)
        await message.answer('Отправьте фото для своей анкеты')
    else:
        await message.answer('Отправьте описание корректно')
        return


@router.message(Register.photo)
async def handle_photo(message: Message, state: FSMContext):
    if validators.photo_validate(message.photo):
        photo = message.photo[-1].file_id
        await state.update_data(photo=photo)
        data = await state.get_data()
        print(data)
        await send_profile(message=message, state=state, data=data, after_register=True)
        await message.answer(text=messages.FINISH_REGISTER, reply_markup=kb_r.menu_keyboard)
        await state.clear()
        return
    else:
        await message.answer('Отправьте фото корректно')
        return

@router.message(F.text == '👤 Моя анкета')
async def send_profile(message: Message, state: FSMContext, data=None, after_register=False):
    await message.answer('Вот ваша анкета: ')

    if not after_register:
        if data['description']:
            await message.answer_photo(
            photo=data['photo'], caption=profile_template(username=data['username'], age=data['age'], city=data['city'],\
            description=data['description'], sex=data['sex'], search_desire=data['search_desire'], searched_by=data['searched_by'])
            , reply_markup=kb_r.profile_keyboard)
    else:
        await message.answer_photo(
            photo=data['photo'], caption=profile_template(username=data['username'], age=data['age'], city=data['city'],\
            description=data['description'], sex=data['sex'], search_desire=data['search_desire'], searched_by=data['searched_by'])
            )
