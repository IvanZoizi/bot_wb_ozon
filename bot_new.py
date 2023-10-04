import asyncio
import logging


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData


class Number(StatesGroup):
    ozon = State()
    wb = State()


logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

bot = Bot('5526766002:AAFGazXTruzsDGJAOfFHhjVUyb8jLij5AlY')
dp = Dispatcher(bot, storage=MemoryStorage())

start_keyboards = types.ReplyKeyboardMarkup(row_width=2)
for i, ii in [['График работы', 'Данные для самостоятельного заказа'],
              ['Где вы находитесь?', 'Сколько стоит доставка?'], ['Как сделать заказ?', 'Как долго ждать доставку?']]:
    start_keyboards.add(types.KeyboardButton(text=i), types.KeyboardButton(text=ii))
start_keyboards.add(types.KeyboardButton(text='Проверить статус моего заказа'))


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer("Доброго времени суток! Я бот-помощник Ex_one Delivery Bot. Чем могу помочь?", reply_markup=start_keyboards)


@dp.message_handler(state=Number.ozon)
async def ozon(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(state=Number.wb)
async def wb(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(content_types=['text'])
async def text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'График работы':
        await message.answer("Работаем каждый день с 9:00 до 17:00")
    elif message.text == 'Где вы находитесь?':
        await message.answer("Мы находимся по ул. Университетская 39А (Парк Шмидта, в здании Газовой службы)")
    elif message.text == 'Сколько стоит доставка?':
        await message.answer("Стоимость доставки от 100 р. за единицу товара, всё зависит от габаритов, веса и ценности товара. Для ценных товаров 7-10% от стоимости товара.")
    elif message.text == 'Как сделать заказ?':
        await message.answer("Вы выбираете интересующие товары и присылаете ссылку в личные сообщения @ex_one1 , заказ товаров осуществляется после оплаты наличными в офисе или переводом на карту.")
    elif message.text == 'Как долго ждать доставку?':
        await message.answer("Доставляем в течении недели, после того как заказ будет доставлен в пункт выдачи в Ростове. После оформления заказа Вы всегда получаете плановую дату доставки.")
    elif message.text == 'Данные для самостоятельного заказа':
        await state.update_data(key=True)
        keyboards = types.ReplyKeyboardMarkup(row_width=2)
        for i, ii in [['Ozon', 'Wildberries'],
                      ['CDEK', 'Почта России'],]:
            keyboards.add(types.KeyboardButton(text=i), types.KeyboardButton(text=ii))
        keyboards.add(types.KeyboardButton(text='Вернуться в главное меню'))
        await message.answer("Выберите:", reply_markup=keyboards)
    elif message.text == 'Проверить статус моего заказа':
        await state.update_data(key=False)
        keyboards = types.ReplyKeyboardMarkup(row_width=2)
        for i, ii in [['Ozon', 'Wildberries']]:
            keyboards.add(types.KeyboardButton(text=i), types.KeyboardButton(text=ii))
        keyboards.add(types.KeyboardButton(text='Вернуться в главное меню'))
        await message.answer("Выберите:", reply_markup=keyboards)
    elif message.text == 'Ozon':
        if data['key']:
            await message.answer("Для заказа укажите Ваше ФИО, затем выберите пункт выдачи, г.РОСТОВ-НА-ДОНУ ул . Гагаринская 18", reply_markup=start_keyboards)
        else:
            await message.answer("Введите номер заказа")
            await Number.ozon.set()
    elif message.text == 'Wildberries':
        if data['key']:
            await message.answer("Для заказа укажите Ваше ФИО, затем выберите пункт выдачи, г.РОСТОВ-НА-ДОНУ ул . Гагаринская 18", reply_markup=start_keyboards)
        else:
            await message.answer("Введите номер заказа")
            await Number.wb.set()
    elif message.text == 'CDEK':
        if data['key']:
            await message.answer("г. РОСТОВ-НА-ДОНУ ул. Таганрогская 112А Получатель: Обушенко Елена Александровна +79900901466", reply_markup=start_keyboards)
    elif message.text == 'Почта России':
        if data['key']:
            await message.answer("г. РОСТОВ-НА-ДОНУ ул.Никулиной 2/161 Индекс:344016 Получатель: Обушенко Елена Александровна +79900901466", reply_markup=start_keyboards)
    elif message.text == 'Вернуться в главное меню':
        await message.answer("Возвращаемся", reply_markup=start_keyboards)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
