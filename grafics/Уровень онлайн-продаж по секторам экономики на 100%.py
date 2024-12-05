import pandas as pd
import matplotlib.pyplot as plt

covid_df = pd.read_csv("Russia-COVID follow up 2020-full data.csv")
russia_2019_df = pd.read_csv("Russia_2019.csv")
types_df = pd.read_excel("types.xlsx")

sectors_of_interest = ['Производство', 'Торговля (опт)', 'Торговля (роз)', 'Услуги', 'Строительство']
filtered_types = types_df[types_df['type'].isin(sectors_of_interest)]

merged_df = pd.merge(russia_2019_df, filtered_types, on='d1a1x', how='inner')
merged_df = pd.merge(covid_df, merged_df, left_on='idstd', right_on='idstd', how='inner')

merged_df['COVc5'] = pd.to_numeric(merged_df['COVc5'], errors='coerce')
average_online_sales = merged_df.groupby('type')['COVc5'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.bar(average_online_sales['type'], average_online_sales['COVc5'], color='blue')
plt.title('Уровень онлайн-продаж по секторам экономики', fontsize=16)
plt.xlabel('Сектора экономики', fontsize=14)
plt.ylabel('Средний уровень онлайн-продаж (%)', fontsize=14)
plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()