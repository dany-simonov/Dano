import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Russia_2019.csv")
df['Объем продаж'] = pd.to_numeric(df['d2'], errors='coerce')
df = df.dropna(subset=['Объем продаж'])

def classify_company(revenue):
    if revenue < 120_000_000:
        return 'Микропредприятие'
    elif revenue < 800_000_000:
        return 'Малое предприятие'
    elif revenue < 2_000_000_000:
        return 'Среднее предприятие'
    else:
        return 'Крупное предприятие'

df['Категория'] = df['Объем продаж'].apply(classify_company)

category_counts = df['Категория'].value_counts()
category_order = ['Микропредприятие', 'Малое предприятие', 'Среднее предприятие', 'Крупное предприятие']
category_counts = category_counts.reindex(category_order)

plt.figure(figsize=(10, 6))
category_counts.plot(kind='bar', color='blue')
plt.title('Количество компаний по категориям', fontsize=16)
plt.xlabel('Категория', fontsize=14)
plt.ylabel('Количество компаний', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()