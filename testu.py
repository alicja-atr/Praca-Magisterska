import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = \
    df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()

# Filtrowanie tylko mieszkańców Wrocławia i poprawną płeć
df_filtered = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna']))
].copy()

# Oblicz liczbę korzyści na osobę
df_filtered['Liczba_korzysci'] = df_filtered[
    'Jakie korzyści dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'
].fillna('').apply(lambda x: len([item for item in x.split(',') if item.strip() != '']))

# Podział na grupy płci
kobiety = df_filtered[df_filtered['Płeć'] == 'Kobieta']['Liczba_korzysci']
mezczyzni = df_filtered[df_filtered['Płeć'] == 'Mężczyzna']['Liczba_korzysci']

# Test Manna-Whitneya
stat, p = mannwhitneyu(kobiety, mezczyzni, alternative='two-sided')
print(f"Test Manna-Whitneya – Liczba dostrzeganych korzyści")
print(f"Statystyka U: {stat:.2f}")
print(f"P-value: {p:.4f}")
print("-" * 40)

# Wykres: rozkład liczby korzyści w obu grupach
plt.figure(figsize=(8,5))
plt.hist(kobiety, bins=range(0, max(kobiety.max(), mezczyzni.max())+2), alpha=0.6, label='Kobiety', color='orchid')
plt.hist(mezczyzni, bins=range(0, max(kobiety.max(), mezczyzni.max())+2), alpha=0.6, label='Mężczyźni', color='cornflowerblue')
plt.title("Rozkład liczby dostrzeganych korzyści (kobiety vs mężczyźni)")
plt.xlabel("Liczba zaznaczonych korzyści")
plt.ylabel("Liczba osób")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

