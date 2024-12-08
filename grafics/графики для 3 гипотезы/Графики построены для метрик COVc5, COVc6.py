import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
covid_df = pd.read_csv("Russia-COVID follow up 2020-full data.csv")
russia_2019_df = pd.read_csv("Russia_2019.csv")
types_df = pd.read_excel("types.xlsx")

# Фильтрация типов
sectors_of_interest = ['Производство', 'Торговля (опт)', 'Торговля (роз)', 'Услуги', 'Строительство']
filtered_types = types_df[types_df['type'].isin(sectors_of_interest)]

# Объединение данных
merged_retail = pd.merge(russia_2019_df, filtered_types, on='d1a1x', how='inner')
merged_df = pd.merge(covid_df, merged_retail, left_on='idstd', right_on='idstd', how='inner')

# Преобразование метрик в числовой формат
metrics_numeric = ['COVc5', 'COVc6']
for metric in metrics_numeric:
    merged_df[metric] = pd.to_numeric(merged_df[metric], errors='coerce')

# Описания метрик
metric_descriptions = {
    'COVc5': 'Какова сейчас доля продаж онлайн?',
    'COVc6': 'Какая доля сотрудников работает удаленно?'
}

# Построение графиков для числовых метрик
for metric in metrics_numeric:
    average_metric = merged_df.groupby('type')[metric].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    plt.bar(average_metric['type'], average_metric[metric], color='blue')
    plt.title(f"{metric} {metric_descriptions[metric]}", fontsize=16)
    plt.xlabel('Сектора экономики', fontsize=14)
    plt.ylabel(f'Средний уровень {metric}', fontsize=14)
    plt.xticks(rotation=45)
    plt.ylim(0, 30)  # Установите пределы до 50%
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()
    plt.show()

print("Графики построены для метрик:", metrics_numeric)