import requests
import fake_useragent

from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
header = {
    'user-agent': user
}

zodiak_sign = {
      'Рак♋': ['cancer', 4],
      'Телец♉': ['taurus', 2],
      'Овен♈': ['aries', 1],
      'Близнецы♊': ['gemini', 3],
      'Весы♎': ['libra', 7],
      'Лев♌': ['leo', 5],
      'Дева♍': ['virgo', 6],
      'Скорпион♏': ['scorpio', 8],
      'Стрелец♐': ['sagittarius', 9],
      'Козерог♑': ['capricorn', 10],
      'Водолей♒': ['aquarius', 11],
      'Рыбы♓': ['pisces', 12]
}


def get_horoscope(sign, gender):
      responce = requests.get(f'https://astrohelper.ru/horoscope/{sign}/', headers=header).text
      soup = BeautifulSoup(responce, 'lxml')
      result = soup.find('div', class_="mt-3").find_all('p')[gender].text
      return result


def check_zodiak(user_zodiak):
      for zodiak in zodiak_sign:
            if zodiak_sign[zodiak][0] == user_zodiak:
                  return [1, zodiak_sign[zodiak][1]]


def get_compatibility(female, male):
    link = f'https://horo.mail.ru/compatibility/zodiac/?gender_1=female&sign_id_1={int(female)}&gender_2=male&sign_id_2={int(male)}'
    responce = requests.get(link, headers=header).text
    soup = BeautifulSoup(responce, 'lxml')
    result = soup.find('div', class_="article__item article__item_alignment_left article__item_html").text
    result1 = soup.find('div', class_="p-item__left-icon-text").text
    return [result, result1]
