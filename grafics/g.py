import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('Russia-COVID follow up 2020-full data.csv')

# Преобразование столбца COVc5 в числовой формат
data['COVc5'] = pd.to_numeric(data['COVc5'], errors='coerce')

# Удаление строк с NaN значениями в COVc5
data = data.dropna(subset=['COVc5'])

# Создание категории для доли онлайн-продаж
data['Доля онлайн-продаж'] = pd.cut(data['COVc5'], bins=[0, 25, 50, 75, 100], labels=['0-25%', '26-50%', '51-75%', '76-100%'])

# Подсчет изменений в продажах по доле онлайн-продаж
sales_change = data.groupby('Доля онлайн-продаж')['COVb2a'].value_counts().unstack().fillna(0)

# Изменение цветов на более подходящие
sales_change.plot(kind='bar', stacked=True, color=['red', 'gray', 'green', 'blue'])
plt.title('Изменения в продажах по доле онлайн-продаж', fontsize=16)
plt.xlabel('Доля онлайн-продаж', fontsize=14)
plt.ylabel('Количество компаний', fontsize=14)
plt.xticks(rotation=0)
plt.legend(title='Изменение продаж', fontsize=12)
plt.grid(axis='y', alpha=0.5)
plt.show()