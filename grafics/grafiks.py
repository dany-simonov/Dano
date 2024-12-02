import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



data = pd.read_csv('Russia-COVID follow up 2020-full data.csv')

online_activity = data['COVc4a'].value_counts()
plt.figure(figsize=(8, 5))
online_activity.plot(kind='bar', color=['lightgreen', 'salmon'])
plt.title('Внедрение онлайн-активности бизнесом')
plt.xlabel('Начали/увеличили активность бизнеса онлайн?')
plt.ylabel('Количество компаний')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.75)
plt.show()