import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Russia-COVID follow up 2020-full data.csv')

df.rename(columns={
    'COVb2a': 'sales_change',
    'COVb2b': 'sales_increase_percentage',
    'COVb2c': 'sales_decrease_percentage',
    'COVc5': 'online_sales_share'
}, inplace=True)

df = df[df['online_sales_share'] != 'Dont know']
df['online_sales_share'] = pd.to_numeric(df['online_sales_share'], errors='coerce')
df = df.dropna(subset=['online_sales_share'])
df = df.sort_values(by='online_sales_share')

# Define the color mapping
color_mapping = {
    'Decrease': 'red',
    'Remain the same': 'blue',
    "Don't know": 'gray',
    'Increase': 'green'
}

plt.figure(figsize=(11, 6))
sns.boxplot(x='online_sales_share', y='sales_change', data=df, palette=color_mapping)
plt.title('Распределение изменений в продажах по доле онлайн-продаж', fontsize=16)
plt.xlabel('Доля онлайн-продаж (%)', fontsize=14)
plt.ylabel('Изменение продаж', fontsize=14)
plt.grid(axis='y', alpha=0.5)
plt.show()