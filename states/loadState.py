from aiogram.dispatcher.filters.state import State, StatesGroup

class Compatibility(StatesGroup):

      female = State()
      male = State()

class NatalnayaKarta(StatesGroup):

      date = State()
      time = State()
      city = State()
      counter = State()