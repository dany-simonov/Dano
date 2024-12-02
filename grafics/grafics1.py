import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv('Russia-COVID follow up 2020-full data.csv')


delivery_counts = data['COVc4b'].value_counts()
plt.figure(figsize=(10, 6))
delivery_counts.plot(kind='bar', color=['blue', 'orange'])
plt.title('Количество компаний, начавших/увеличивших доставку или предоставление на вынос', fontsize=16)
plt.xlabel('Начали/увеличили доставку или предоставление на вынос?', fontsize=14)
plt.ylabel('Количество компаний', fontsize=14)
plt.xticks(rotation=0)  # Убираем наклон меток оси X
plt.grid(axis='y', alpha=0.5)  # Добавление сетки по оси Y для удобства чтения
plt.show()