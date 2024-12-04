import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Russia_2019.csv")
df['Численность работников'] = pd.to_numeric(df['l1'], errors='coerce')
df = df.dropna(subset=['Численность работников'])

def classify_company(employees):
    if employees <= 15:
        return 'Микропредприятие'
    elif employees <= 100:
        return 'Малое предприятие'
    elif employees <= 250:
        return 'Среднее предприятие'
    else:
        return 'Крупное предприятие'

df['Категория'] = df['Численность работников'].apply(classify_company)

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