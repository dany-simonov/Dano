import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('Russia-COVID follow up 2020-full data.csv')
remote_work_counts = data['COVc4c'].value_counts()


plt.figure(figsize=(10, 6))
sns.barplot(x=remote_work_counts.index, y=remote_work_counts.values, palette='Set2')
plt.title('Доступность удаленной работы для персонала', fontsize=16)
plt.xlabel('Начали/увеличили доступность удаленной работы?', fontsize=14)
plt.ylabel('Количество компаний', fontsize=14)
plt.xticks(fontsize=12)  # Размер шрифта меток оси X
plt.yticks(fontsize=12) 
plt.grid(axis='y', alpha=0.75) 
plt.show()