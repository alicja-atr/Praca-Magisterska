import pandas as pd
from scipy.stats import mannwhitneyu
import seaborn as sns
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()
df['Poparcie'] = df['Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?'].str.strip().str.capitalize()

# Filtr: tylko mieszkańcy Wrocławia i kobieta/mężczyzna, bez "Trudno powiedzieć"
df = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna'])) &
    (df['Poparcie'] != 'Trudno powiedzieć')
]

# Przypisanie wartości liczbowych poziomom poparcia
mapa_poparcia = {
    'Zdecydowanie tak': 4,
    'Raczej tak': 3,
    'Raczej nie': 2,
    'Zdecydowanie nie': 1
}
df['Poparcie_num'] = df['Poparcie'].map(mapa_poparcia)

# Podział na grupy płci
poparcie_k = df[df['Płeć'] == 'Kobieta']['Poparcie_num']
poparcie_m = df[df['Płeć'] == 'Mężczyzna']['Poparcie_num']

# Test Manna–Whitneya
stat, p = mannwhitneyu(poparcie_k, poparcie_m, alternative='two-sided')

# Wyniki
print("=== Test Manna–Whitneya ===")
print(f"Liczba kobiet: {len(poparcie_k)}, Liczba mężczyzn: {len(poparcie_m)}")
print(f"Statystyka U = {stat:.3f}")
print(f"p-value = {p:.4f}")
print("-----------------------------------------------------")

# Wykres
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='Płeć', y='Poparcie_num', palette='Set2')
plt.title("Poziom poparcia dla łąk miejskich wg płci (U Manna–Whitneya)")
plt.ylabel("Poziom poparcia (1–4)")
plt.xlabel("Płeć respondenta")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

