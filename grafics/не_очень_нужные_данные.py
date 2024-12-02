import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Russia-COVID follow up 2020-full data.csv')

# Удаляем строки с пустыми значениями в COVe1b и COVe1c
data = data[data['COVe1b'].notna() & data['COVe1c'].notna()]

# Классификация по категориям для продаж в кредит
data['category_sales'] = data['COVe1b'].replace({
    'Increase': 'Increase',
    'Decrease': 'Decrease',
    'Remain the same': 'Remain the same',
    "Don't know": "Don't know"
})

# Классификация по категориям для покупок в кредит
data['category_purchases'] = data['COVe1c'].replace({
    'Increase': 'Increase',
    'Decrease': 'Decrease',
    'Remain the same': 'Remain the same',
    "Don't know": "Don't know"
})

# Подсчет количества компаний в каждой категории для продаж в кредит
counts_sales = data['category_sales'].value_counts().reindex(['Increase', 'Decrease', 'Remain the same', "Don't know"], fill_value=0)

# Подсчет количества компаний в каждой категории для покупок в кредит
counts_purchases = data['category_purchases'].value_counts().reindex(['Increase', 'Decrease', 'Remain the same', "Don't know"], fill_value=0)

# Создание графика
plt.figure(figsize=(12, 6))
bar_width = 0.35
x = range(len(counts_sales.index))

# График для данных о продажах в кредит
plt.bar(x, counts_sales.values, width=bar_width, color='blue', label='Продажи в кредит')

# График для данных о покупках в кредит
plt.bar([p + bar_width for p in x], counts_purchases.values, width=bar_width, color='green', label='Покупки в кредит')

plt.xlabel('Категории изменений')
plt.ylabel('Количество компаний')
plt.title('Изменения в продажах и покупках в кредит')
plt.xticks([p + bar_width / 2 for p in x], counts_sales.index)
plt.legend()
plt.grid(axis='y')

plt.tight_layout()
plt.show()