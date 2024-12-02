import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('Russia-COVID follow up 2020-full data.csv')

data['COVc5'] = pd.to_numeric(data['COVc5'], errors='coerce') 
data = data.dropna(subset=['COVc5'])

plt.figure(figsize=(10, 6))
sns.histplot(data['COVc5'], bins=20, color='darkblue', kde=True, edgecolor='black')
plt.title('Распределение доли онлайн-продаж')
plt.xlabel('Доля онлайн-продаж (%)')
plt.ylabel('Количество компаний')
plt.grid(axis='y', alpha=0.75)

# Отображение графика
plt.show()