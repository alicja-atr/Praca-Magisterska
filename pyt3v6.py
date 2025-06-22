import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Nazwy kolumn (upewnij się, że dokładnie takie są w pliku)
poparcie_col = "Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?"
estetyka_col = "Który rodzaj zieleni miejskiej uważa Pan/Pani za bardziej estetyczny?"
plec_col = "Płeć"
mieszkaniec_col = "Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?"

# Czyszczenie i filtrowanie
df[poparcie_col] = df[poparcie_col].str.strip().str.capitalize()
df[estetyka_col] = df[estetyka_col].str.strip().str.capitalize()
df[plec_col] = df[plec_col].str.strip().str.capitalize()
df[mieszkaniec_col] = df[mieszkaniec_col].str.strip().str.capitalize()

# Filtr: tylko mieszkańcy Wrocławia i kobieta/mężczyzna
df = df[
    (df[mieszkaniec_col] == 'Tak') &
    (df[plec_col].isin(['Kobieta', 'Mężczyzna'])) &
    (df[estetyka_col].isin(['Łąki miejskie', 'Tradycyjne trawniki', 'Oba rodzaje podobają mi się tak samo'])) &
    df[poparcie_col].notna() &
    df[estetyka_col].notna()
]

# Kolejność kategorii poparcia
poparcie_kategorie = ['Zdecydowanie tak', 'Raczej tak', 'Raczej nie', 'Zdecydowanie nie', 'Trudno powiedzieć']

# Tworzenie tabeli kontyngencji
contingency = pd.crosstab(df[estetyka_col], df[poparcie_col]).reindex(columns=poparcie_kategorie, fill_value=0)

# Test chi-kwadrat
chi2, p, dof, expected = chi2_contingency(contingency)

# Wyniki testu
print("=== Test Chi²: Poparcie vs Estetyka ===")
print("Tablica kontyngencji:")
print(contingency)
print(f"\nStatystyka Chi² = {chi2:.3f}")
print(f"p-value = {p:.4f}")
print(f"Stopnie swobody = {dof}")

print("\nWniosek:")
if p < 0.05:
    print("=> Istnieje statystycznie istotna zależność między postrzeganą estetyką zieleni a poparciem dla łąk.")
else:
    print("=> Brak statystycznie istotnej zależności między postrzeganą estetyką zieleni a poparciem.")

# Normalizacja do wykresu procentowego
contingency_norm = contingency.div(contingency.sum(axis=1), axis=0)

# Wykres
ax = contingency_norm.plot(kind='bar', stacked=True, colormap='YlGn', figsize=(10, 6))

# Etykiety procentowe
for i, row in enumerate(contingency_norm.values):
    cum_height = 0
    for j, val in enumerate(row):
        if val > 0:
            ax.text(i, cum_height + val / 2, f"{val * 100:.1f}%", ha='center', va='center', color='black', fontsize=8)
            cum_height += val

plt.title("Rozkład poparcia względem postrzeganej estetyki zieleni miejskiej")
plt.ylabel("Proporcje odpowiedzi")
plt.xlabel("Preferowany typ zieleni")
plt.xticks(rotation=45)
plt.legend(title="Poparcie dla łąk", bbox_to_anchor=(1.05, 1))
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

