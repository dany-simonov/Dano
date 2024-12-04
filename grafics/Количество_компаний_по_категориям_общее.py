import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Russia_2019.csv")
df['Численность работников'] = pd.to_numeric(df['l1'], errors='coerce')
df['Объем продаж'] = pd.to_numeric(df['d2'], errors='coerce')
df = df.dropna(subset=['Численность работников', 'Объем продаж'])

def classify_company(row):
    if row['Численность работников'] > 250 or row['Объем продаж'] >= 2_000_000_000:
        return 'Крупное предприятие'
    elif row['Численность работников'] > 100 or row['Объем продаж'] >= 800_000_000:
        return 'Среднее предприятие'
    elif row['Численность работников'] > 15 or row['Объем продаж'] >= 120_000_000:
        return 'Малое предприятие'
    else:
        return 'Микропредприятие'

df['Категория'] = df.apply(classify_company, axis=1)

category_counts = df['Категория'].value_counts()
category_order = ['Микропредприятие', 'Малое предприятие', 'Среднее предприятие', 'Крупное предприятие']
category_counts = category_counts.reindex(category_order)

for category, count in category_counts.items():
    print(f'{category}: {count} компаний')

plt.figure(figsize=(10, 6))
category_counts.plot(kind='bar', color='blue')
plt.title('Количество компаний по категориям', fontsize=16)
plt.xlabel('Категория', fontsize=14)
plt.ylabel('Количество компаний', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()