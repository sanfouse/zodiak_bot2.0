import fake_useragent
import requests
from bs4 import BeautifulSoup

url = 'https://astrohelper.ru/natalnaja-karta/result.php'
user = fake_useragent.UserAgent().random
header = {
    'user-agent': user
}

def get_natalnaja_karta(date='01.01.2000', time='10:00', city='Москва', dolgota='', shirina='', counter=1):
      data = {
            'day': date.split('.')[0],
            'month': date.split('.')[1],
            'year': date.split('.')[2],
            'hour': time.split(':')[0],
            'minute': time.split(':')[1],
            'query': city,
            'dolgota': dolgota,
            'shirina': shirina
      }
      responce = requests.post(url, headers=header, data=data).text
      soup = BeautifulSoup(responce, 'lxml')
      block = soup.find('div', id='natals').text
      result = [block.split('\n\n')[counter]][0] + '\n'
      result_2 = [block.split('\n\n')[counter + 1]][0]
      if len(result) < 50:
            result = result + result_2
            del result_2
      return [result]

