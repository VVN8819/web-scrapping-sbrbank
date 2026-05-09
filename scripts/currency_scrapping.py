import requests
from bs4 import BeautifulSoup
import time
import json
from pathlib import Path

# ============ Создаём путь к папке "data" внутри текущего проекта ==================
data_dir = Path(__file__).parent / "data"
data_dir.mkdir(exist_ok=True)  # Создаём папку, если нет
output_json = data_dir / 'sbrbank_currency_rate.json'

# =============== Подключаемся к "https://www.cbr.ru/" ====================
url = "https://www.cbr.ru/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
} # обход блокировок
response = requests.get(url)
print(f'Статус-код: {response.status_code}')

time.sleep(1) # обход блокировок

# Добавим парсер из текста страницы
soup = BeautifulSoup(response.text, 'lxml')
print(f'Источник: {soup.title.text}')

# список для хранения результатов
report = []

# ======================= Находим валюту ==============================
currencies = soup.find_all('div', class_='main-indicator_rate')

# классы для фильтрации
cur_class_list = ['col-md-2', 'col-xs-9']
class_list = ['_left', 'mono-num']

# Ищем блок
for currency in currencies:
    # Валюты: ищем ВСЕ div с классом "col-md-2" и "col-xs-9"
    class_name = currency.find('div', class_=cur_class_list)

    # Если нашли — вытаскиваем данные
    if class_name:
        currency_name = class_name.get_text(strip=True) if class_name else "Не найдено"

        # Курсы: ищем ВСЕ div с классом "_left" и "mono-num"
        rate_divs = currency.find_all('div', class_=class_list)

        current_rate = rate_divs[0].get_text(strip=True) if len(rate_divs) > 0 else "N/A"
        previous_rate = rate_divs[1].get_text(strip=True) if len(rate_divs) > 1 else "N/A"
        
        # словарь результата
        currency_data = {
            "name": currency_name,
            "current_rate": current_rate,
            "previous_rate": previous_rate
        }
        report.append(currency_data)

        print(f'\nВалюта: {currency_name}')
        print(f'- Был вчера: {current_rate}')
        print(f'- Текущий курс: {previous_rate}')
        time.sleep(1) # обход блокировок

with open(output_json, 'w', encoding='utf-8') as f:
  json.dump(report, f, ensure_ascii=False, indent=2)
  print(f'Сохранено в: {output_json}')

print(f'Данные сохранены в файл: {output_json}')