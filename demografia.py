import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns

# 1️⃣ Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# 2️⃣ Czyszczenie kolumn tekstowych
cols_to_clean = ['Płeć', 'Wiek', 'Wykształcenie', 'Status zawodowy',
                 'Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?', 
                 'Czy wie Pan/Pani czym są łąki miejskie?', 
                 'Który rodzaj zieleni miejskiej uważa Pan/Pani za bardziej estetyczny?']
for col in cols_to_clean:
    df[col] = df[col].str.strip().str.capitalize()

# 3️⃣ Filtrowanie próby badawczej
df = df[
    (df['Płeć'].isin(['Mężczyzna', 'Kobieta'])) &
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Czy wie Pan/Pani czym są łąki miejskie?'] == 'Tak') &
    (df['Który rodzaj zieleni miejskiej uważa Pan/Pani za bardziej estetyczny?'].isin(
        ['Łąki miejskie', 'Oba rodzaje podobają mi się tak samo', 'Tradycyjne trawniki']))
]

# 4️⃣ Lista zmiennych demograficznych do testów
demographic_vars = ['Płeć', 'Wiek', 'Wykształcenie', 'Status zawodowy']

# 4a️⃣ Mapa zmiennych na formy dopełniaczowe (dla tytułów)
label_map = {
    'Płeć': 'płci',
    'Wiek': 'wieku',
    'Wykształcenie': 'wykształcenia',
    'Status zawodowy': 'statusu zawodowego'
}

# 5️⃣ Funkcja testu chi² z filtracją określonych kategorii
def chi_squared_test(var):
    df_sub = df.copy()

    # Filtry dla konkretnych zmiennych
    if var == 'Wykształcenie':
        df_sub = df_sub[~df_sub['Wykształcenie'].isin(['Wolę nie podawać', 'Zasadnicze zawodowe'])]

    if var == 'Status zawodowy':
        df_sub = df_sub[~df_sub['Status zawodowy'].isin(['Inne', 'Bezrobotny'])]

    contingency_table = pd.crosstab(df_sub[var], df_sub['Który rodzaj zieleni miejskiej uważa Pan/Pani za bardziej estetyczny?'])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    print(f"\n==== Test Chi² dla: {var} ====")
    print("Tablica kontyngencji:")
    print(contingency_table)
    print(f"Chi² = {chi2:.3f}, p-value = {p:.4f}, df = {dof}")
    print("-" * 40)
    
    # Wersja z normalizacją (proporcje)
    contingency_table_norm = contingency_table.div(contingency_table.sum(axis=1), axis=0)

    # Tworzenie wykresu słupkowego z etykietami
    ax = contingency_table_norm.plot(kind='bar', stacked=True, colormap='viridis', figsize=(8,5))

    # Dodawanie etykiet z procentami
    for i, row in enumerate(contingency_table_norm.values):
        cum_height = 0
        for j, val in enumerate(row):
            if val > 0:
                ax.text(i, cum_height + val/2, f"{val*100:.1f}%", ha='center', va='center', color='white', fontsize=9)
                cum_height += val

    plt.title(f"Rozkład preferencji estetycznych względem {label_map.get(var, var)}")
    plt.ylabel("Proporcja odpowiedzi")
    plt.xlabel(var)
    plt.legend(title="Preferencja estetyczna", bbox_to_anchor=(1.05, 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# 6️⃣ Przeprowadzenie testów
for var in demographic_vars:
    chi_squared_test(var)

