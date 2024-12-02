import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Russia-COVID follow up 2020-full data.csv')
df['COVc5'] = pd.to_numeric(df['COVc5'], errors='coerce')  
df = df.dropna(subset=['COVc5'])  
df['Доля онлайн-продаж'] = pd.cut(df['COVc5'], bins=[0, 25, 50, 75, 100], labels=['0-25%', '26-50%', '51-75%', '76-100%'])
sales_change = df.groupby('Доля онлайн-продаж')['COVb2a'].value_counts(normalize=True).unstack(fill_value=0) * 100  

sales_change.plot(kind='bar', stacked=True, color=['red', 'gray', 'green', 'blue'], figsize=(10, 6))

plt.title('Изменения в продажах по доле онлайн-продаж', fontsize=16)
plt.xlabel('Доля онлайн-продаж (%)', fontsize=14)
plt.ylabel('Процент компаний', fontsize=14)
plt.xticks(rotation=0)  
plt.legend(title='Изменение продаж', fontsize=12)
plt.grid(axis='y', alpha=0.5)

plt.ylim(0, 100)  

plt.show()