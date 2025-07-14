from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

import utils
import keyboards as kb
import validators
from states import Register

router = Router()


class RegistrationHandler:
    def __init__(self, message: Message, state: FSMContext):
        self.message = message
        self.state = state
    
    async def start_registration(self):
        await self.state.set_state(Register.sex)
        await self.message.answer('Введите ваш пол', reply_markup=kb.sex_choice)
    
    async def handle_sex(self):
        if validators.sex_validate(self.message.text):
            sex_value = 0 if self.message.text == 'Мужской' else 1
            await self.state.update_data(sex=sex_value)
            await self.state.set_state(Register.search_desire)
            await self.message.answer('Чьи анкеты вы хотитите смотреть?', reply_markup=kb.search_desire)
            return
        await self.message.answer('Введите пол корректно', reply_markup=kb.sex_choice)
        return 
    
    async def handle_search_desire(self):
        if validators.search_desire_validate(self.message.text):
            if self.message.text == 'Парней':
                search_desire = 0
            elif self.message.text == 'Девушек':
                search_desire = 1
            else:
                search_desire = 2
            
            await self.state.update_data(search_desire=search_desire)
            await self.state.set_state(Register.name)
            await self.message.answer('Введите ваше имя')
            return
        await self.message.answer('Выберите корректно.\nЧьи анкеты вы хотитите смотреть?', reply_markup=kb.search_desire)
        return 
    
    async def handle_name(self):
        if validators.name_validate(self.message.text):
            await self.state.update_data(name=self.message.text)
            await self.state.set_state(Register.age)
            await self.message.answer('Введите ваш возраст')
            return
        await self.message.answer('Введите имя корректно (до 20 символов)')
        return 
    
    async def handle_age(self):
        if validators.age_validate(self.message.text):
            await self.state.update_data(age=int(self.message.text))
            await self.state.set_state(Register.city)
            await self.message.answer('Введите ваш город')
            return
        await self.message.answer('Введите возраст корректно')
        return 
    
    async def handle_city(self):
        if validators.city_validate(self.message.text):
            await self.state.update_data(city=self.message.text)
            await self.state.set_state(Register.description)
            await self.message.answer('Напишите описание для своей анкеты')
            return
        await self.message.answer('Введите город корректно')
        return 
    
    async def handle_description(self):
        if validators.description_validate(self.message.text):
            await self.state.update_data(description=self.message.text)
            await self.state.set_state(Register.photo)
            await self.message.answer('Отправьте фото для вашей анкеты')
            return
        await self.message.answer('Введите описание корректно')
        return 
    
    async def handle_photo(self):
        if validators.photo_validate(self.message.photo):
            await self.state.update_data(photo=self.message.photo[-1].file_id)
            await self.send_profile()
            return
        await self.message.answer('Отправьте фото корректно')
        return 
    
    async def send_profile(self):
        profile_data = await self.state.get_data()
        await self.message.answer('Регистрация завершена. Вот ваша анкета: ')
        await self.message.answer_photo(
            photo=profile_data['photo'],
            caption=f"{profile_data['name']}, {profile_data['age']}, {profile_data['city']}\n\n{profile_data['description']}"
        )


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(text=utils.welcome_greet(message.from_user.first_name), reply_markup=kb.register_button)


@router.callback_query(F.data == 'signup')
async def start_reg(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    handler = RegistrationHandler(callback.message, state)
    await handler.start_registration()


@router.message(Register.sex)
async def handle_sex(message: Message, state: FSMContext):
    handler = RegistrationHandler(message, state)
    await handler.handle_sex()


@router.message(Register.search_desire)
async def handle_search_desire(message: Message, state: FSMContext):
    handler = RegistrationHandler(message, state)
    await handler.handle_search_desire()


@router.message(Register.name)
async def handle_name(message: Message, state: FSMContext):
    handler = RegistrationHandler(message, state)
    await handler.handle_name()


@router.message(Register.age)
async def handle_age(message: Message, state: FSMContext):
    handler = RegistrationHandler(message, state)
    await handler.handle_age()


@router.message(Register.city)
async def handle_city(message: Message, state: FSMContext):
    handler = RegistrationHandler(message, state)
    await handler.handle_city()


@router.message(Register.description)
async def handle_description(message: Message, state: FSMContext):
    handler = RegistrationHandler(message, state)
    await handler.handle_description()


@router.message(Register.photo)
async def handle_photo(message: Message, state: FSMContext):
    handler = RegistrationHandler(message, state)
    await handler.handle_photo()