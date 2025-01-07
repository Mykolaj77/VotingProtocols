import pandas as pd
import re
from datetime import datetime
import requests
import os

# Завантажуємо файл з веб-сайту
url = 'https://rgk.vote.mod.gov.ua/protocol.txt'
response = requests.get(url)
response.raise_for_status()
lines = response.text.split('\n')

# Обробляємо дані
parsed_data = []
for line in lines:
    line = line.strip().replace('"', '')  # Видаляємо лапки
    parts = line.split('\t')  # Розбиваємо по табуляції

    if len(parts) >= 2:
        timestamp = parts[0]
        ip = parts[1]
        rest = ' '.join(parts[2:])

        # Парсимо ключі N, B, S, V
        n_match = re.search(r'N=(\d+)', rest)
        b_match = re.search(r'B=([A-Z0-9]+)', rest)
        s_match = re.search(r'S=([A-Z0-9]+)', rest)
        v_match = re.search(r'V=([\d,]+)', rest)

        n = n_match.group(1) if n_match else None
        b = b_match.group(1) if b_match else None
        s = s_match.group(1) if s_match else None
        v = v_match.group(1).split(',') if v_match else []

        parsed_data.append([timestamp, ip, n, b, s, v])

# Створюємо DataFrame
df = pd.DataFrame(parsed_data, columns=['Timestamp', 'IP', 'N', 'B', 'S', 'V'])

# Отримуємо останню дату і час у даних
latest_timestamp = pd.to_datetime(df['Timestamp']).max()
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Підрахунок кількості виборців
total_voters = len(df)

# Список кандидатів
candidates = [
    'Нишпорка Олена Іванівна', 'Соловйов Микита Олександрович', 'Шуба Анастасія Вадимівна',
    'Романчук Андрій Богданович', 'Бріт Ореста Павлівна', 'Русаков Сергій Олександрович',
    'Гудименко Юрій Володимирович', 'Штанков Микита Володимирович', 'Акопян Рудольф Володимирович',
    'Гришко Вероніка Віталіївна', 'Юрченко Анна Ігорівна', 'Мельник Руслан Дмитрович',
    'Олівінський Олександр Вікторович', 'Свинаренко Олексій Олександрович', 'Кутний Роман Антонович',
    'Розум Олег Володимирович', 'Левченко В’ячеслав Васильович', 'Рибалко Тетяна Сергіївна',
    'Плоска Ганна Віталіївна', 'Пшеничний Давид Олександрович', 'Яциняк Єлизавета Тарасівна',
    'Костецький Максим Юрійович', 'Ніколаєнко Тетяна Володимировна', 'Трегуб Олена Миколаївна',
    'Корольов Ігор Сергійович', 'Рябека Євгенія Олександрівна', 'Слесаренко Євгеній Ігорович',
    'Осінчук Остап Мирославович', 'Мітєва Катерина Олександрівна', 'Попович Інна Юріївна',
    'Біщук Віктор Павлович', 'Масюк Віталій Володимирович', 'Чернов Олег Валерійович',
    'Калинчук Анна Сергіївна', 'Геращенко Олександр Володимирович', 'Кривошея Геннадій Григорович',
    'Ярова Богдана Едуардівна', 'Даценко Катерина Андріївна', 'Микитюк Антон Сергійович',
    'Прудковських Віктор В’ячеславович'
]

# Зіставлення номерів кандидатів з їх іменами
candidate_dict = {str(i + 1): candidates[i] for i in range(len(candidates))}

# Формуємо список голосів з іменами кандидатів
df['V_named'] = df['V'].apply(lambda x: [candidate_dict.get(v, f'Кандидат {v}') for v in x])

# Підрахунок голосів за іменами
votes_named = df['V_named'].explode().value_counts()

# Список 15 кандидатів з найбільшою кількістю голосів
top_candidates_named = votes_named.head(15)
other_candidates_named = votes_named[15:]

# Формуємо таблицю результатів
top_table = pd.DataFrame({'Кандидат': top_candidates_named.index, 'Голосів': top_candidates_named.values})
other_table = pd.DataFrame({'Кандидат': other_candidates_named.index, 'Голосів': other_candidates_named.values})

# Зберігаємо таблицю результатів у файл
result_file = 'voting_results.csv'
final_table = pd.concat([top_table, other_table])
final_table.to_csv(result_file, index=False)

# Вивід результатів
print(f'Запит виконано: {current_time}')
print(f'Останній голос: {latest_timestamp}')
print(f'Загальна кількість виборців: {total_voters}')
print('Топ-15 кандидатів за кількістю голосів:')
print(top_table)
print('Решта кандидатів:')
print(other_table)
print(f"Оброблені дані збережено у {result_file}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
