import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
covid_df = pd.read_csv("Russia-COVID follow up 2020-full data.csv")
russia_2019_df = pd.read_csv("Russia_2019.csv")
types_df = pd.read_excel("types.xlsx")

# Классификация компаний
russia_2019_df['Численность работников'] = pd.to_numeric(russia_2019_df['l1'], errors='coerce')
russia_2019_df['Объем продаж'] = pd.to_numeric(russia_2019_df['d2'], errors='coerce')
russia_2019_df = russia_2019_df.dropna(subset=['Численность работников', 'Объем продаж'])

def classify_company(row):
    if row['Численность работников'] > 250 or row['Объем продаж'] >= 2_000_000_000:
        return 'Крупное предприятие'
    elif row['Численность работников'] > 100 or row['Объем продаж'] >= 800_000_000:
        return 'Среднее предприятие'
    elif row['Численность работников'] > 15 or row['Объем продаж'] >= 120_000_000:
        return 'Малое предприятие'
    else:
        return 'Микропредприятие'

russia_2019_df['Категория'] = russia_2019_df.apply(classify_company, axis=1)

# Фильтрация типов
production_types = types_df[types_df['type'] == 'Производство']
merged_df = pd.merge(russia_2019_df, production_types, on='d1a1x', how='inner')
merged_df = pd.merge(covid_df, merged_df, left_on='idstd', right_on='idstd', how='inner')

# Построение графика для метрики _2012_2019_h5
metric_h5 = '_2012_2019_h5'
plt.figure(figsize=(12, 6))

# Получаем процентные значения для метрики по категориям
percentage_data_h5 = merged_df.groupby('Категория')[metric_h5].value_counts(normalize=True).unstack().fillna(0) * 100
percentage_data_h5 = percentage_data_h5.reindex(['Микропредприятие', 'Малое предприятие', 'Среднее предприятие', 'Крупное предприятие'])  # Убедитесь, что сектора в нужном порядке

# Убедитесь, что все категории присутствуют
for category in ['Yes', 'No', "Don't know"]:
    if category not in percentage_data_h5.columns:
        percentage_data_h5[category] = 0

# Построение столбчатой диаграммы
percentage_data_h5 = percentage_data_h5[['Yes', 'No', "Don't know"]]  # Убедитесь, что порядок категорий правильный
colors_h5 = ['green', 'red', 'blue']  # Цвета для Yes, No, Don't know
percentage_data_h5.plot(kind='bar', stacked=True, color=colors_h5)

plt.title(f"{metric_h5} В течение последних трех лет, происходило ли введение новых/улучшение старых процессов?", fontsize=10)
plt.xlabel('Категория бизнеса', fontsize=14)
plt.ylabel('Процент', fontsize=14)
plt.ylim(0, 100)  # Установите пределы до 100%
plt.grid(axis='y', alpha=0.5)
plt.legend(title='Ответы', loc='upper right')

plt.tight_layout()
plt.show()