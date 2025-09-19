# visualize.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('books_data.xlsx')
plt.figure(figsize=(8,5))
sns.histplot(df['price'], bins=15, kde=True)
plt.title("Price distribution")
plt.xlabel("Price (£)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
