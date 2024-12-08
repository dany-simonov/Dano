import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
covid_df = pd.read_csv("Russia-COVID follow up 2020-full data.csv")
russia_2019_df = pd.read_csv("Russia_2019.csv")
types_df = pd.read_excel("types.xlsx")

# Определение описаний метрик
metric_descriptions = {
    'COVc4a': 'Начали/увеличили активность бизнеса онлайн?',
    'COVc4b': 'Начали/увеличили доставку или предоставление товаров и услуг на вынос?',
    'COVc4c': 'Начали/увеличили доступность удаленной работы для своего персонала?',
    'COVc5': 'Какова сейчас доля продаж онлайн?',
    'COVc6': 'Какая доля сотрудников работает удаленно?',
    'c22b': 'Есть ли у фирмы веб-сайт?',
    '_2012_2019_h5': 'В течение последних трех лет, происходило ли введение новых/улучшение старых процессов?',
}

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

# Фильтрация типов для сектора "Услуги"
service_types = types_df[types_df['type'] == 'Услуги']
merged_df = pd.merge(russia_2019_df, service_types, on='d1a1x', how='inner')
merged_df = pd.merge(covid_df, merged_df, left_on='idstd', right_on='idstd', how='inner')

# Метрики для построения графиков
metrics_categorical = ['COVc4a', 'COVc4b', 'COVc4c', 'c22b']
metrics_numerical = ['COVc5', 'COVc6']

# Построение графиков для категориальных метрик
for metric in metrics_categorical:
    plt.figure(figsize=(12, 6))
    
    # Получаем процентные значения для метрики по категориям
    percentage_data = merged_df.groupby('Категория')[metric].value_counts(normalize=True).unstack().fillna(0) * 100
    percentage_data = percentage_data.reindex(['Микропредприятие', 'Малое предприятие', 'Среднее предприятие', 'Крупное предприятие'])  # Убедитесь, что сектора в нужном порядке

    # Убедитесь, что все категории присутствуют
    for category in ['Yes', 'No', "Don't know"]:
        if category not in percentage_data.columns:
            percentage_data[category] = 0

    # Построение столбчатой диаграммы
    percentage_data = percentage_data[['Yes', 'No', "Don't know"]]  # Убедитесь, что порядок категорий правильный
    colors = ['green', 'red', 'blue']  # Цвета для Yes, No, Don't know
    percentage_data.plot(kind='bar', stacked=True, color=colors)
    
    plt.title(f"{metric} {metric_descriptions[metric]}", fontsize=10)  # Изменен размер шрифта заголовка
    plt.xlabel('Категория бизнеса', fontsize=14)
    plt.ylabel('Процент', fontsize=14)
    plt.ylim(0, 100)  # Установите пределы до 100%
    plt.grid(axis='y', alpha=0.5)
    plt.legend(title='Ответы', loc='upper right')
    
    plt.tight_layout()
    plt.show()

# Построение графиков для числовых метрик
for metric in metrics_numerical:
    plt.figure(figsize=(12, 6))
    
    # Получаем средние значения для метрики по категориям
    merged_df[metric] = pd.to_numeric(merged_df[metric], errors='coerce')
    average_digitalization = merged_df.groupby('Категория')[metric].mean().reset_index()

    # Упорядочивание категорий
    average_digitalization['Категория'] = pd.Categorical(average_digitalization['Категория'], categories=['Микропредприятие', 'Малое предприятие', 'Среднее предприятие', 'Крупное предприятие'], ordered=True)
    average_digitalization = average_digitalization.sort_values('Категория')

    # Построение графика
    plt.bar(average_digitalization['Категория'], average_digitalization[metric], color='blue')
    plt.title(f"{metric} {metric_descriptions[metric]}", fontsize=10)  # Изменен размер шрифта заголовка
    plt.xlabel('Категория бизнеса', fontsize=14)
    plt.ylabel('Средний уровень (%)', fontsize=14)
    plt.xticks(rotation=45)
    plt.ylim(0, 50)  # Установите пределы до 50%
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()
    plt.show()