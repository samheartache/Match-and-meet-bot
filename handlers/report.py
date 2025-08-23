from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.requests import add_report, set_watched
from middlewares.reports_middleware import ReportMiddleware

router = Router()
router.callback_query.middleware(ReportMiddleware())


@router.callback_query(F.data.startswith('report_user'))
async def report_user(callback: CallbackQuery):
    reported_id = int(callback.data.split(':')[1])
    await add_report(tg_id=reported_id)
    await callback.answer('✅ Жалоба успешно оставлена')
    await callback.message.answer(text='✅ Вы оставили жалобу на пользователя')
    await set_watched(tg_id=reported_id, liked_id=callback.from_user.id)
    await callback.message.delete()