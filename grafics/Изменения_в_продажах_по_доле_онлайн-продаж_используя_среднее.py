import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('Russia-COVID follow up 2020-full data.csv')
df['COVc5'] = pd.to_numeric(df['COVc5'], errors='coerce')  
df = df.dropna(subset=['COVc5'])  
df['Доля онлайн-продаж'] = pd.cut(df['COVc5'], bins=[0, 25, 50, 75, 100], labels=['0-25%', '26-50%', '51-75%', '76-100%'])

# Convert COVb2b and COVb2c to numeric, coercing errors to NaN
df['COVb2b'] = pd.to_numeric(df['COVb2b'], errors='coerce')
df['COVb2c'] = pd.to_numeric(df['COVb2c'], errors='coerce')

# Calculate average growth and decline
growth_decline = {}
for interval in df['Доля онлайн-продаж'].cat.categories:
    subset = df[df['Доля онлайн-продаж'] == interval]
    avg_growth = subset['COVb2b'].dropna().mean()
    avg_decline = subset['COVb2c'].dropna().mean()
    growth_decline[interval] = {
        'avg_growth': avg_growth,
        'avg_decline': avg_decline
    }
    # Вывод средних значений в консоль
    print(f'Интервал: {interval}, Средний прирост: {avg_growth:.1f}%, Среднее падение: {avg_decline:.1f}%')

sales_change = df.groupby('Доля онлайн-продаж')['COVb2a'].value_counts(normalize=True).unstack(fill_value=0) * 100  

ax = sales_change.plot(kind='bar', stacked=True, color=['red', 'gray', 'green', 'blue'], figsize=(10, 6))

plt.title('Изменения в продажах по доле онлайн-продаж', fontsize=16)
plt.xlabel('Доля онлайн-продаж (%)', fontsize=14)
plt.ylabel('Процент компаний', fontsize=14)
plt.xticks(rotation=0)  
plt.grid(axis='y', alpha=0.5)

# Move the legend to the lower left corner
plt.legend(title='Изменение продаж', fontsize=12, loc='lower left')

plt.ylim(0, 100)  

# Annotate the bars with average growth and decline
for i, interval in enumerate(growth_decline.keys()):
    avg_growth = growth_decline[interval]['avg_growth']
    avg_decline = growth_decline[interval]['avg_decline']
    if pd.notna(avg_growth):
        red_height = sales_change.loc[interval, 'Decrease']
        green_height = sales_change.loc[interval, 'Increase']
        ax.text(i, red_height + (green_height / 2.1), f'{avg_growth:.1f}%', ha='center', color='black')
    if pd.notna(avg_decline):
        red_height = sales_change.loc[interval, 'Decrease']
        ax.text(i, red_height / 2, f'{avg_decline:.1f}%', ha='center', color='black')

plt.show()