import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('Russia-COVID follow up 2020-full data.csv')

plt.figure(figsize=(10, 6))
sns.histplot(data['COVb2a'], bins=20, color='lightgreen', kde=True)

plt.title('Изменение продаж в последнем месяце по сравнению с аналогичным месяцем 2019 года')
plt.xlabel('Изменение продаж')
plt.ylabel('Количество компаний')
plt.grid(axis='y', alpha=0.75)
plt.show()
