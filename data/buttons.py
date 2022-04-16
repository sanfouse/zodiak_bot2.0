from aiogram import types

markup = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text='Рак♋', callback_data='cancer'),
    types.InlineKeyboardButton(text='Телец♉', callback_data='taurus'),
    types.InlineKeyboardButton(text='Близнецы♊', callback_data='gemini'),
    types.InlineKeyboardButton(text='Весы♎', callback_data='libra'),
    types.InlineKeyboardButton(text='Лев♌', callback_data='leo'),
    types.InlineKeyboardButton(text='Дева♍', callback_data='virgo'),
    types.InlineKeyboardButton(text='Скорпион♏', callback_data='scorpio'),
    types.InlineKeyboardButton(text='Стрелец♐', callback_data='sagittarius'),
    types.InlineKeyboardButton(text='Козерог♑', callback_data='capricorn'),
    types.InlineKeyboardButton(text='Водолей♒', callback_data='aquarius'),
    types.InlineKeyboardButton(text='Рыбы♓', callback_data='pisces'),
    types.InlineKeyboardButton(text='Овен♈', callback_data='aries'),
    types.InlineKeyboardButton(text='Назад', callback_data='cancel'))

keyboard = types.InlineKeyboardMarkup(row_width=2).add(
      types.InlineKeyboardButton(text='Совместимость💞', callback_data='Совместимость'), 
      types.InlineKeyboardButton(text='Гороскоп⛎', callback_data='Гороскоп'),
      types.InlineKeyboardButton(text='Натальная карта🀄️ (beta)', callback_data='Натальная карта'))

cancel_markup = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text='Назад', callback_data='cancel'))

map_markup = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text='Назад', callback_data='back'),
    types.InlineKeyboardButton(text='Следующая страница', callback_data='next'),
    types.InlineKeyboardButton(text='Выход', callback_data='cancel'))

map_markup2 = types.InlineKeyboardMarkup().add(
    types.InlineKeyboardButton(text='Следующая страница', callback_data='next'),
    types.InlineKeyboardButton(text='Выход', callback_data='cancel'))