import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie podstawowe
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = \
    df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()

df['Płeć'] = df['Płeć'].str.strip().str.capitalize()

# Filtr: tylko mieszkańcy Wrocławia i osoby z podaną płcią
df = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna']))
]

# Czyszczenie kolumn wieloodpowiedziowych
df['Korzyści'] = df['Jakie korzyści dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'].fillna('').str.strip()
df['Wady'] = df['Jakie wady dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'].fillna('').str.strip()

# Liczenie liczby odpowiedzi w obu pytaniach
df['Liczba_korzysci'] = df['Korzyści'].apply(lambda x: len([ans for ans in x.split(',') if ans.strip() != '']))
df['Liczba_wad'] = df['Wady'].apply(lambda x: len([ans for ans in x.split(';') if ans.strip() != '']))

# Wyświetlenie podstawowych statystyk
print(df[['Liczba_korzysci', 'Liczba_wad']].describe())

# Korelacja Spearmana
corr, p_value = spearmanr(df['Liczba_korzysci'], df['Liczba_wad'])

print("\nWspółczynnik korelacji Spearmana:")
print(f"Korelacja: {corr:.3f}, p-value: {p_value:.4f}")

# Wizualizacja - wykres rozrzutu
plt.figure(figsize=(8,6))
plt.scatter(df['Liczba_korzysci'], df['Liczba_wad'], alpha=0.6)
plt.title("Zależność: liczba dostrzeganych korzyści vs wad (tylko mieszkańcy Wrocławia)")
plt.xlabel("Liczba korzyści")
plt.ylabel("Liczba wad")
plt.grid(True)
plt.tight_layout()
plt.show()

