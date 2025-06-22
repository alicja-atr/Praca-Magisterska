import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie kolumn
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()

# Filtrowanie tylko mieszkańców Wrocławia i osób z podaną płcią
df = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna']))
]

# Czyszczenie kolumny wad
df['Wady'] = df['Jakie wady dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'].fillna('').str.strip()

# Rozdzielanie odpowiedzi
df['Wady_lista'] = df['Wady'].str.split(',')

# Spłaszczamy i czyścimy wpisy
all_faults = df['Wady_lista'].explode().str.strip().str.lower()

# Lista dozwolonych odpowiedzi
dozwolone_wady = [
    'mogą wywoływać alergie',
    'przyciągają owady',
    'nieestetyczny wygląd',
    'są rzadziej koszone',
    'utrudniają widoczność kierowcom',
    'nie dostrzegam wad'
]

# Filtrowanie i liczenie
fault_counts = all_faults[all_faults.isin(dozwolone_wady)].value_counts()

# Sortowanie malejąco
fault_counts = fault_counts.sort_values(ascending=False)

# Wykres
plt.figure(figsize=(10,6))
bars = fault_counts.plot(kind='bar', color='salmon')
plt.title("Częstość wyboru wybranych wad łąk miejskich")
plt.xlabel("Wada")
plt.ylabel("Liczba wskazań")
plt.xticks(rotation=45, ha='right')

# Dodanie liczby wskazań na słupkach
for i, value in enumerate(fault_counts):
    plt.text(i, value + 0.5, str(value), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

