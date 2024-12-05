import pandas as pd
import matplotlib.pyplot as plt

covid_df = pd.read_csv("Russia-COVID follow up 2020-full data.csv")
russia_2019_df = pd.read_csv("Russia_2019.csv")
types_df = pd.read_excel("types.xlsx")

russia_2019_df['Численность работников'] = pd.to_numeric(russia_2019_df['l1'], errors='coerce')
russia_2019_df['Объем продаж'] = pd.to_numeric(russia_2019_df['d2'], errors='coerce')
russia_2019_df = russia_2019_df.dropna(subset=['Численность работников', 'Объем продаж'])

def classify_company(row):
    if row['Численность работников'] > 250 or row['Объем продаж'] >= 2_000_000_000:
        return 'Крупное предприятие'
    elif row['Численность работников'] > 100 or row['Объем продаж'] >= 800_000_000:
        return 'Среднее предприятие'
    elif row['Численность работников'] > 15 or row['Объем продаж'] >= 120_000_000:
        return 'Малое предприятие'
    else:
        return 'Микропредприятие'

russia_2019_df['Категория'] = russia_2019_df.apply(classify_company, axis=1)

retail_trade_types = types_df[types_df['type'] == 'Торговля (роз)']
wholesale_trade_types = types_df[types_df['type'] == 'Торговля (опт)']

merged_retail = pd.merge(russia_2019_df, retail_trade_types, on='d1a1x', how='inner')
merged_wholesale = pd.merge(russia_2019_df, wholesale_trade_types, on='d1a1x', how='inner')

merged_df = pd.concat([merged_retail, merged_wholesale])
merged_df = pd.merge(covid_df, merged_df, left_on='idstd', right_on='idstd', how='inner')

merged_df['COVc5'] = pd.to_numeric(merged_df['COVc5'], errors='coerce')

average_digitalization = merged_df.groupby('Категория')['COVc5'].mean().reset_index()

category_order = ['Микропредприятие', 'Малое предприятие', 'Среднее предприятие', 'Крупное предприятие']
average_digitalization['Категория'] = pd.Categorical(average_digitalization['Категория'], categories=category_order, ordered=True)
average_digitalization = average_digitalization.sort_values('Категория')

overall_digitalization = merged_df['COVc5'].mean()

print("Уровень цифровизации по категориям бизнеса в торговле:")
for index, row in average_digitalization.iterrows():
    print(f"{row['Категория']}: {row['COVc5']:.2f}%")

print(f"Общий уровень цифровизации в торговле: {overall_digitalization:.2f}%")

plt.figure(figsize=(12, 6))
plt.bar(average_digitalization['Категория'], average_digitalization['COVc5'], color='blue')
plt.title('Уровень цифровизации по категориям бизнеса в секторе "Торговля" (опт + роз)', fontsize=16)
plt.xlabel('Категория бизнеса', fontsize=14)
plt.ylabel('Средний уровень цифровизации (%)', fontsize=14)
plt.xticks(rotation=45)
plt.ylim(0, 50)
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.show()