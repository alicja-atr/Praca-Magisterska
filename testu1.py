import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = \
    df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()

# Filtrowanie mieszkańców Wrocławia i płci binarnej
df_filtered = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna']))
].copy()

# Obliczenie liczby korzyści
df_filtered['Liczba_korzysci'] = df_filtered[
    'Jakie korzyści dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'
].fillna('').apply(lambda x: len([item for item in x.split(',') if item.strip() != '']))

# Test Manna-Whitneya
kobiety = df_filtered[df_filtered['Płeć'] == 'Kobieta']['Liczba_korzysci']
mezczyzni = df_filtered[df_filtered['Płeć'] == 'Mężczyzna']['Liczba_korzysci']
stat, p = mannwhitneyu(kobiety, mezczyzni, alternative='two-sided')

print(f"Test Manna-Whitneya – Liczba dostrzeganych korzyści")
print(f"Statystyka U: {stat:.2f}")
print(f"P-value: {p:.4f}")
print("-" * 40)

# Wykres
plt.figure(figsize=(8,6))
sns.boxplot(x='Płeć', y='Liczba_korzysci', data=df_filtered, palette=['orchid', 'cornflowerblue'])
sns.stripplot(x='Płeć', y='Liczba_korzysci', data=df_filtered, color='gray', alpha=0.5, jitter=True)
plt.title("Liczba dostrzeganych korzyści z łąk miejskich (wg płci)")
plt.xlabel("Płeć")
plt.ylabel("Liczba korzyści")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

