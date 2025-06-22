import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie kolumn
poparcie_col = "Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?"
df[poparcie_col] = df[poparcie_col].str.strip().str.capitalize()
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()
df['Wiek'] = df['Wiek'].str.strip().str.capitalize()
df['Wykształcenie'] = df['Wykształcenie'].str.strip().str.capitalize()
df['Status zawodowy'] = df['Status zawodowy'].str.strip().str.capitalize()
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()

# Filtr: mieszkańcy Wrocławia i osoby z poprawnie podaną płcią
df = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna']))
]

# Kolejność kategorii odpowiedzi
kategorie = ['Zdecydowanie tak', 'Raczej tak', 'Raczej nie', 'Zdecydowanie nie', 'Trudno powiedzieć']

# Rozkład ogólny (dla wszystkich mieszkańców)
rozkład = df[poparcie_col].value_counts().reindex(kategorie, fill_value=0)

# Wykres ogólny
plt.figure(figsize=(8, 5))
rozkład.plot(kind='bar', color='seagreen')
plt.title("Rozkład odpowiedzi na pytanie o poparcie dla łąk miejskich")
plt.ylabel("Liczba odpowiedzi")
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

label_map = {
    'Płeć': 'płci',
    'Wiek': 'wieku',
    'Wykształcenie': 'wykształcenia',
    'Status zawodowy': 'statusu zawodowego'
}

# Funkcja testu Chi² z etykietami procentowymi i poprawionym tytułem
def chi_squared_test(df, demografia_col):
    df_sub = df.copy()

    # Filtrowanie kategorii
    if demografia_col == 'Wykształcenie':
        df_sub = df_sub[~df_sub['Wykształcenie'].isin(['Wolę nie podawać', 'Zasadnicze zawodowe'])]
    if demografia_col == 'Status zawodowy':
        df_sub = df_sub[~df_sub['Status zawodowy'].isin(['Inne', 'Bezrobotny'])]

    # Tabela kontyngencji
    contingency = pd.crosstab(df_sub[demografia_col], df_sub[poparcie_col]).reindex(columns=kategorie, fill_value=0)

    # Test Chi²
    chi2, p, dof, expected = chi2_contingency(contingency)

    print(f"\n=== Test Chi² dla: {demografia_col} ===")
    print("Tablica kontyngencji:")
    print(contingency)
    print(f"Chi²: {chi2:.3f}, p-value: {p:.4f}, df: {dof}")
    print("-" * 40)

    # Normalizacja
    contingency_norm = contingency.div(contingency.sum(axis=1), axis=0)

    # Wykres z etykietami procentowymi
    ax = contingency_norm.plot(kind='bar', stacked=True, colormap='viridis', figsize=(10, 6))

    for i, row in enumerate(contingency_norm.values):
        cum_height = 0
        for j, val in enumerate(row):
            if val > 0:
                ax.text(i, cum_height + val / 2, f"{val * 100:.1f}%", ha='center', va='center', color='white', fontsize=8)
                cum_height += val

    # ✔️ Zmieniony tytuł wykresu:
    title_suffix = label_map.get(demografia_col, demografia_col.lower())
    plt.title(f"Rozkład poparcia względem {title_suffix}")
    plt.ylabel("Proporcje")
    plt.xlabel(demografia_col)
    plt.xticks(rotation=45)
    plt.legend(title="Odpowiedź", bbox_to_anchor=(1.05, 1))
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
# Uruchomienie testów dla zmiennych demograficznych
for col in ['Płeć', 'Wiek', 'Wykształcenie', 'Status zawodowy']:
    chi_squared_test(df, col) 
