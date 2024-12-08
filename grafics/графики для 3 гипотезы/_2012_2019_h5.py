import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
russia_2019_df = pd.read_csv("Russia_2019.csv")
types_df = pd.read_excel("types.xlsx")

# Фильтрация типов
sectors_of_interest = ['Производство', 'Торговля (опт)', 'Торговля (роз)', 'Услуги', 'Строительство']
filtered_types = types_df[types_df['type'].isin(sectors_of_interest)]

# Объединение данных
merged_dataframes = []
for sector in sectors_of_interest:
    sector_types = filtered_types[filtered_types['type'] == sector]
    merged_sector = pd.merge(russia_2019_df, sector_types, on='d1a1x', how='inner')
    merged_dataframes.append(merged_sector)

merged_df = pd.concat(merged_dataframes)

# Описания метрики
metric = '_2012_2019_h5'
metric_description = 'В течение последних трех лет, происходило ли введение новых/улучшение старых процессов?'

# Построение графика для метрики
plt.figure(figsize=(14, 6))

# Получаем процентные значения для метрики по секторам
percentage_data = merged_df.groupby('type')[metric].value_counts(normalize=True).unstack().fillna(0) * 100
percentage_data = percentage_data.reindex(sectors_of_interest)  # Убедитесь, что сектора в нужном порядке

# Убедитесь, что все категории присутствуют
colors = {'Yes': 'green', 'No': 'red', "Don't know (spontaneous)": 'blue'}
for category in colors.keys():
    if category not in percentage_data.columns:
        percentage_data[category] = 0

# Построение столбчатой диаграммы
percentage_data = percentage_data[colors.keys()]  # Убедитесь, что порядок категорий правильный
percentage_data.plot(kind='bar', stacked=True, color=[colors[val] for val in percentage_data.columns])

plt.title(f"{metric} {metric_description}", fontsize=10)
plt.xlabel('Сектора экономики', fontsize=14)
plt.ylabel('Процент', fontsize=14)
plt.ylim(0, 100)  # Установите пределы до 100%
plt.grid(axis='y', alpha=0.5)

# Добавление легенды
plt.legend(percentage_data.columns, loc='upper right')

plt.tight_layout()
plt.show()  # Открываем новое окно и ждем его закрытия

print("График построен для метрики:", metric)