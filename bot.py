from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from data.buttons import *
from data.config import BOT_TOKEN
from data.messages import start_text
from states.loadState import Compatibility, NatalnayaKarta
from utils.filter import check_message, message_filter
from utils.horoscope import check_zodiak, get_compatibility, get_horoscope
from utils.natalnaja_karta import get_natalnaja_karta

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

### Menu ###

@dp.message_handler(commands='start')
async def start_message(message: types.message.Message):
  await message.answer(text=start_text, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda m: m.data == 'Гороскоп')
async def start_message(message: types.CallbackQuery):
      await message.message.edit_text('Выберите знак зодиака: \n\n 👇🏻👇🏻👇🏻', reply_markup=markup)


@dp.callback_query_handler(lambda m: m.data == 'Совместимость')
async def compatibility_message(message: types.CallbackQuery):
      await message.message.edit_text('Выберите знак зодиака *женщины*💃: \n\n 👇🏻👇🏻👇🏻', reply_markup=markup, parse_mode="Markdown")
      await Compatibility.female.set()


@dp.callback_query_handler(lambda m: m.data == 'Натальная карта')
async def natalnaya_karta_message(message: types.CallbackQuery):
      await message.message.edit_text('Введите *дату* рождения:👇🏻👇🏻👇🏻\n\n _Пример ввода: 01.01.2000_', parse_mode="Markdown", reply_markup=cancel_markup)
      await NatalnayaKarta.date.set()


@dp.callback_query_handler(lambda m: bool(check_zodiak(m.data)))
async def horoscope(call: types.CallbackQuery):
    markup_1 = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text='•Женщина🧍‍♀️', callback_data='h'),
    types.InlineKeyboardButton(text='Мужчина🧍‍♂️', callback_data=call.data + '1'),
    types.InlineKeyboardButton(text='Назад', callback_data='cancel'))
    await call.message.edit_text(text=f'*Ваш гороскоп на сегодня:*\n_{get_horoscope(sign=call.data, gender=2)}_',
    parse_mode="Markdown", reply_markup=markup_1)


@dp.callback_query_handler(lambda m: m.data[-1] == '1' and bool(check_zodiak(m.data[:-1])))
async def horoscope(call: types.CallbackQuery):
  markup_1 = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text='•Мужчина🧍‍♂️', callback_data='h'),
    types.InlineKeyboardButton(text='Женщина🧍‍♀️', callback_data=call.data[:-1]),
    types.InlineKeyboardButton(text='Назад', callback_data='cancel'))
  await call.message.edit_text(text=f'*Ваш гороскоп на сегодня:*\n_{get_horoscope(sign=call.data[:-1], gender=1)}_',
    parse_mode="Markdown", reply_markup=markup_1)

### States ###

@dp.callback_query_handler(lambda m: message_filter(m.data), state=Compatibility.female)
async def love(message: types.CallbackQuery, state: FSMContext):
    female = check_zodiak(message.data)[-1]
    try:
        await state.update_data(
            {
                'female': female
            }
        )
        await message.message.edit_text(text=f'Выберите знак зодиака *мужчины*🕺: \n\n 👇🏻👇🏻👇🏻', reply_markup=markup, parse_mode="Markdown")
        await Compatibility.next()
    except ValueError:
      await state.finish() 


@dp.callback_query_handler(lambda m: message_filter(m.data), state=Compatibility.male)
async def love1(message:types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    female = data.get('female')
    male = check_zodiak(message.data)[-1]
    markup_cancel = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text='Назад', callback_data='cancel'))

    try:
      result = get_compatibility(female, male)
      await message.message.edit_text(text=f'_{result[0]}_\n\n\n*💞Совместимость в процентах: {result[1]}💞*', parse_mode="Markdown", reply_markup=markup_cancel)
      await state.finish()
    except ValueError:
        await state.finish()


@dp.callback_query_handler(lambda m: message_filter(m.data), state=NatalnayaKarta.date)
@dp.message_handler(lambda m: check_message(m.text), state=NatalnayaKarta.date)
async def natalny_map_date(message:types.Message, state: FSMContext):
    date = message.text
    try:
      await state.update_data(
        {
          'date': date
        }
      )
      await message.answer('Введите *время* рождения: 👇🏻👇🏻👇🏻\n\n _Пример ввода: 10:00_',
            reply_markup=cancel_markup, parse_mode="Markdown")
      await NatalnayaKarta.next()
    except Exception as ex:
      print(ex)
      await message.edit_text(start_text, reply_markup=keyboard, parse_mode="Markdown")
      await state.finish()


@dp.callback_query_handler(lambda m: message_filter(m.data), state=NatalnayaKarta.time)
@dp.message_handler(lambda m: check_message(m.text), state=NatalnayaKarta.time)
async def natalny_map_time(message:types.Message, state: FSMContext):
    time = message.text
    try:
      await state.update_data(
        {
          'time': time
        }
      )
      await message.answer('Введите *город*: 👇🏻👇🏻👇🏻\n\n _Пример ввода: Москва_',
             reply_markup=cancel_markup, parse_mode="Markdown")
      await NatalnayaKarta.next()
    except Exception as ex:
      print(ex)
      await message.edit_text(start_text, reply_markup=keyboard, parse_mode="Markdown")
      await state.finish()


@dp.callback_query_handler(lambda m: message_filter(m.data), state=NatalnayaKarta.city)
@dp.message_handler(state=NatalnayaKarta.city)
async def natalny_map_city(message:types.Message, state: FSMContext):
    city_user = message.text
    await state.update_data(
      {
        'city': city_user,
        'counter': 1
      } 
    )
    data = await state.get_data()
    date = data.get('date')
    time = data.get('time')
    city = data.get('city')
    try:
      await message.answer(text=get_natalnaja_karta(date=date, time=time, city=city)[0],
            reply_markup=map_markup2)
      await NatalnayaKarta.next()
    except Exception as ex:
      print(ex)
      await message.edit_text(start_text, reply_markup=keyboard, parse_mode="Markdown")
      await state.finish()


### Buttons ###
@dp.callback_query_handler(lambda m: m.data == 'cancel')
async def cancel(message: types.CallbackQuery):
  await message.message.edit_text(start_text, reply_markup=keyboard, parse_mode="Markdown")


@dp.callback_query_handler(lambda m: m.data == 'cancel', state=Compatibility)
async def cancel_compatibility(message: types.CallbackQuery, state: FSMContext):
  await message.message.edit_text(start_text, reply_markup=keyboard, parse_mode="Markdown")
  await state.finish()


@dp.callback_query_handler(lambda m: m.data == 'cancel', state=NatalnayaKarta)
async def cancel_natalny_map(message: types.CallbackQuery, state: FSMContext):
  await message.message.edit_text(start_text, reply_markup=keyboard, parse_mode="Markdown")
  await state.finish()


@dp.message_handler(lambda m: check_message(m.text) == False, state=NatalnayaKarta)
async def cancel_natalny_map(message: types.CallbackQuery, state: FSMContext):
  await message.answer(start_text + '\n\n_Неверный ввод_', reply_markup=keyboard, parse_mode="Markdown")
  await state.finish()


@dp.callback_query_handler(lambda m: m.data == 'next', state=NatalnayaKarta.counter)
async def next_natalny_map(message: types.CallbackQuery, state: FSMContext):
  data = await state.get_data()
  date = data.get('date')
  time = data.get('time')
  city = data.get('city')
  counter = data.get('counter')
  counter += 1
  await state.update_data(
    {'counter': counter}
  )

  try:
    if counter == 1:
      await message.message.edit_text(text=get_natalnaja_karta(date=date, time=time, city=city, counter=counter)[0],
             reply_markup=map_markup2)
    else:
      await message.message.edit_text(text=get_natalnaja_karta(date=date, time=time, city=city, counter=counter)[0],
             reply_markup=map_markup)
  except Exception:
    await message.message.edit_text(text=start_text, reply_markup=keyboard, parse_mode="Markdown")
    await state.finish()


@dp.callback_query_handler(lambda m: m.data == 'back', state=NatalnayaKarta.counter)
async def back_natalny_map(message: types.CallbackQuery, state: FSMContext):
  data = await state.get_data()
  date = data.get('date')
  time = data.get('time')
  city = data.get('city')
  counter = data.get('counter')
  counter -= 1
  await state.update_data(
    {'counter': counter}
  )

  try:
    if counter == 1:
      await message.message.edit_text(text=get_natalnaja_karta(date=date, time=time, city=city, counter=counter)[0], 
            reply_markup=map_markup2)
    else:
      await message.message.edit_text(text=get_natalnaja_karta(date=date, time=time, city=city, counter=counter)[0], 
            reply_markup=map_markup)
  except Exception:
    await message.message.edit_text(text=start_text, reply_markup=keyboard, parse_mode="Markdown")
    await state.finish()


if __name__ == '__main__':
  executor.start_polling(dp)