import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie kluczowych kolumn
df['Który rodzaj zieleni miejskiej uważa Pan/Pani za bardziej estetyczny?'] = \
    df['Który rodzaj zieleni miejskiej uważa Pan/Pani za bardziej estetyczny?'].str.strip().str.capitalize()

df['Jakie wady dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'] = \
    df['Jakie wady dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'].fillna('').str.strip()

# Dodatkowe czyszczenie kolumn do filtrów
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = \
    df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()

df['Płeć'] = df['Płeć'].str.strip().str.capitalize()

# Filtr: mieszkańcy Wrocławia oraz osoby z poprawnie podaną płcią
df = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna']))
]

# Tworzymy nową kolumnę binarną: czy wskazano "Nieestetyczny wygląd"
df['Wada_Nieestetyczny'] = df['Jakie wady dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)']\
    .str.contains('Nieestetyczny wygląd', case=False)

# Interesują nas tylko osoby, które odpowiedziały na oba pytania
df_valid = df[
    df['Który rodzaj zieleni miejskiej uważa Pan/Pani za bardziej estetyczny?'].isin(
        ['Łąki miejskie', 'Oba rodzaje podobają mi się tak samo', 'Tradycyjne trawniki'])
]

# Tworzymy tabelę kontyngencji
contingency = pd.crosstab(
    df_valid['Który rodzaj zieleni miejskiej uważa Pan/Pani za bardziej estetyczny?'],
    df_valid['Wada_Nieestetyczny']
)

# Test chi-kwadrat
chi2, p, dof, expected = chi2_contingency(contingency)

# Wyniki testu
print("==== Test Chi² dla preferencji estetycznych vs nieestetyczny wygląd ====")
print("Tablica kontyngencji:")
print(contingency)
print(f"Chi2: {chi2:.3f}, p-value: {p:.4f}, stopnie swobody: {dof}")
print("-" * 40)

# Wykres pomocniczy
contingency_norm = contingency.div(contingency.sum(1), axis=0)

# Wykres z procentami
ax = contingency_norm.plot(kind='bar', stacked=True, colormap='viridis', figsize=(10,6))

# Dodanie etykiet z procentami
for i, (idx, row) in enumerate(contingency_norm.iterrows()):
    cumulative = 0
    for j, val in enumerate(row):
        if val > 0:
            ax.text(
                i, 
                cumulative + val / 2, 
                f"{val*100:.1f}%", 
                ha='center', 
                va='center', 
                color='white', 
                fontsize=10
            )
            cumulative += val

# Ustawienia wykresu
plt.title("Postrzeganie estetyki łąk w kontekście preferencji trawników")
plt.ylabel("Proporcje")
plt.xlabel("Preferencje estetyczne")
plt.xticks(rotation=45)
plt.legend(title="Czy wskazano 'Nieestetyczny wygląd'", labels=['Nie', 'Tak'], bbox_to_anchor=(1.05, 1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

