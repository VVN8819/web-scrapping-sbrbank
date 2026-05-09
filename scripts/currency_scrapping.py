import requests

# Сохраняем URL
url = "https://www.cbr.ru/"

# GET-запрос к серверу
response = requests.get(url)

# Проверяем статус (200 - "OK")
print(f'Статус-код: {response.status_code}')