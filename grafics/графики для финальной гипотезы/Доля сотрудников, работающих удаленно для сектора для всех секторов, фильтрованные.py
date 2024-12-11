import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_y_scale(data):
    # Получаем высоту самого высокого столбца
    hist, _ = np.histogram(data, bins=range(-100, 101, 20) if 'income_change' in data.name else range(0, 101, 10))
    max_height = max(hist)
    
    # Добавляем 20% к максимальной высоте и округляем до ближайшего десятка
    max_y = int(np.ceil(max_height * 1.2 / 10.0)) * 10
    
    # Вычисляем шаг для получения примерно 10 делений
    step = max_y // 8
    # Округляем шаг до ближайшего числа кратного 5
    step = int(np.ceil(step / 5.0)) * 5
    
    return step, max_y

# Загрузка данных
exclude_df = pd.read_csv("exclude_idst.csv")
covid_df = pd.read_csv("Russia-COVID follow up 2020-full data.csv")
russia_2019_df = pd.read_csv("Russia_2019.csv")
types_df = pd.read_excel("types.xlsx")

# Обработка данных по изменению дохода
def process_income_change(row):
    if row['COVb2a'] == 'Increase':
        return pd.to_numeric(row['COVb2b'], errors='coerce')
    elif row['COVb2a'] == 'Decrease':
        return -pd.to_numeric(row['COVb2c'], errors='coerce')
    return np.nan

covid_df['income_change'] = covid_df.apply(process_income_change, axis=1)
covid_df['COVc6'] = pd.to_numeric(covid_df['COVc6'].replace("Don't know", np.nan), errors='coerce')

# Объединение данных
merged_df = pd.merge(covid_df, russia_2019_df, on='idstd', how='inner')
merged_df = pd.merge(merged_df, types_df, on='d1a1x', how='inner')

# Фильтрация
filtered_df = merged_df[~merged_df['idstd'].isin(exclude_df['idstd'])]

# Получение уникальных секторов
sectors = filtered_df['type'].unique()

# Построение графиков
for sector in sectors:
    sector_data = filtered_df[filtered_df['type'] == sector].copy()
    
    # График изменения дохода
    plt.figure(figsize=(12, 6))
    valid_data = sector_data[sector_data['income_change'].notna()]
    
    if len(valid_data) > 0:
        plt.hist(valid_data['income_change'], bins=range(-100, 101, 20), color='blue', edgecolor='black')
        plt.title(f"Изменение дохода для сектора: {sector}", fontsize=10)
        plt.xlabel('Изменение дохода (%)', fontsize=14)
        plt.ylabel('Количество компаний', fontsize=14)
        plt.xticks(range(-100, 101, 20))
        
        step, max_y = get_y_scale(valid_data['income_change'])
        plt.yticks(range(0, max_y + step, step))
        
        plt.grid(axis='y', alpha=0.5)
        plt.tight_layout()
    plt.show()

    # График удаленной работы
    plt.figure(figsize=(12, 6))
    valid_data = sector_data[sector_data['COVc6'].notna()]
    
    if len(valid_data) > 0:
        plt.hist(valid_data['COVc6'], bins=range(0, 101, 10), color='green', edgecolor='black')
        plt.title(f"COVc6 Доля сотрудников, работающих удаленно для сектора: {sector}", fontsize=10)
        plt.xlabel('Доля сотрудников, работающих удаленно (%)', fontsize=14)
        plt.ylabel('Количество компаний', fontsize=14)
        plt.xticks(range(0, 101, 10))
        
        step, max_y = get_y_scale(valid_data['COVc6'])
        plt.yticks(range(0, max_y + step, step))
        
        plt.grid(axis='y', alpha=0.5)
        plt.tight_layout()
    plt.show()
