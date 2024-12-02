import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('Russia-COVID follow up 2020-full data.csv')
print(df.columns)
print(df.head())
df['Состояние компании'] = df['COVb0'].map({
    'Open': 1,
    'Temporarily closed': 0
})
 
df['Изменение продаж'] = df['COVb2a'].map({
    'Выросли': 1,
    'Остались прежними': 0,
    'Сократились': -1
})

# Преобразование доли онлайн-продаж в числовое значение
df['Доля онлайн-продаж'] = df['COVc5']

# Удаление строк с некорректными значениями
correlation_data = df[['COVb0', 'COVb2a', 'COVb2b', 'COVb2c', 'COVc5']].apply(pd.to_numeric, errors='coerce')
correlation_data = correlation_data.dropna()

correlation_matrix = correlation_data.corr()

# Построение тепловой карты
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Корреляция между метриками', fontsize=16)
plt.show()
