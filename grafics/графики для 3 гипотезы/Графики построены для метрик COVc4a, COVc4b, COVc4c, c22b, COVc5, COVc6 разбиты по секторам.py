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
merged_dataframes = []
for sector in sectors_of_interest:
    sector_types = filtered_types[filtered_types['type'] == sector]
    merged_sector = pd.merge(russia_2019_df, sector_types, on='d1a1x', how='inner')
    merged_dataframes.append(merged_sector)

merged_df = pd.concat(merged_dataframes)
merged_df = pd.merge(covid_df, merged_df, left_on='idstd', right_on='idstd', how='inner')

# Описания метрик
metric_descriptions = {
    'COVc4a': 'Начали/увеличили активность бизнеса онлайн?',
    'COVc4b': 'Начали/увеличили доставку или предоставление товаров и услуг на вынос?',
    'COVc4c': 'Начали/увеличили доступность удаленной работы для своего персонала?',
    'c22b': 'Есть ли у фирмы веб-сайт?'
}

# Построение графиков для всех метрик, разделенных по секторам экономики
all_metrics = ['COVc4a', 'COVc4b', 'COVc4c', 'c22b']
colors = {'Yes': 'green', 'No': 'red', "Don't know": 'blue'}

for metric in all_metrics:
    plt.figure(figsize=(14, 8))
    
    # Получаем процентные значения для категориальных метрик по секторам
    percentage_data = merged_df.groupby('type')[metric].value_counts(normalize=True).unstack().fillna(0) * 100
    percentage_data = percentage_data.reindex(sectors_of_interest)  # Убедитесь, что сектора в нужном порядке

    # Убедитесь, что все категории присутствуют
    for category in colors.keys():
        if category not in percentage_data.columns:
            percentage_data[category] = 0

    # Построение столбчатой диаграммы
    percentage_data = percentage_data[colors.keys()]  # Убедитесь, что порядок категорий правильный
    percentage_data.plot(kind='bar', stacked=True, color=[colors[val] for val in percentage_data.columns])
    
    plt.title(f"{metric} {metric_descriptions[metric]}", fontsize=10)
    plt.xlabel('Сектора экономики', fontsize=14)
    plt.ylabel('Процент', fontsize=14)
    plt.ylim(0, 100)  # Установите пределы до 100%
    plt.grid(axis='y', alpha=0.5)
    
    # Добавление легенды
    plt.legend(percentage_data.columns, loc='upper right')
    
    plt.tight_layout()
    plt.show()  # Открываем новое окно и ждем его закрытия

print("Графики построены для метрик:", all_metrics)