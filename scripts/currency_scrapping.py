import requests
from bs4 import BeautifulSoup

url = "https://www.cbr.ru/"
response = requests.get(url)
print(f'Статус-код: {response.status_code}')

# Добавим парсер из текста страницы
soup = BeautifulSoup(response.text, 'lxml')
print(f'Источник: {soup.title.text}')

# ======================= Находим валюту ==============================
currencies = soup.find_all('div', class_='main-indicator_rate')

# Ищем блок
for currency in currencies:
  cur_class_list = ['col-md-2', 'col-xs-9']
  class_name = currency.find('div', class_=cur_class_list)

  # Если нашли — вытаскиваем данные
  if class_name:

    currency_name = class_name.get_text(strip=True) if class_name else "Не найдено"

    # Курсы: ищем ВСЕ div с классом "_left" и "mono-num"
    class_list = ['_left', 'mono-num']
    rate_divs = currency.find_all('div', class_=class_list)

    current_rate = rate_divs[0].get_text(strip=True) if len(rate_divs) > 0 else "N/A"
    previous_rate = rate_divs[1].get_text(strip=True) if len(rate_divs) > 1 else "N/A"

    print(f'\nВалюта: {currency_name}')
    print(f'- Был вчера: {current_rate}')
    print(f'- Текущий курс: {previous_rate}')

