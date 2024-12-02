import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('Russia-COVID follow up 2020-full data.csv')

company_status = data['COVb0'].value_counts()
plt.figure(figsize=(10, 6))
company_status.plot(kind='bar', color=sns.color_palette('Set1'))
plt.title('Текущее состояние компаний')
plt.xlabel('Состояние компании')
plt.ylabel('Количество компаний')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.75)
plt.show()