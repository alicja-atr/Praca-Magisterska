import pandas as pd
from scipy.stats import kruskal
import seaborn as sns
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie i filtracja danych
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()
df['Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?'] = df['Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?'].str.strip().str.capitalize()

# Filtrowanie
df = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna'])) &
    (df['Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?'] != 'Trudno powiedzieć')
]

# Lista tylko wybranych wad
wady_docelowe = [
    'Mogą wywoływać alergie',
    'Przyciągają owady',
    'Nieestetyczny wygląd',
    'Są rzadziej koszone',
    'Utrudniają widoczność kierowcom'
]

# Przetwarzanie kolumny z wadami
df['Wady'] = df['Jakie wady dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'].fillna('')
df['Wady_lista'] = df['Wady'].str.split(',').apply(lambda x: [i.strip() for i in x if i.strip() in wady_docelowe])
df['Liczba_wad'] = df['Wady_lista'].apply(len)

# Grupowanie po poziomie poparcia
grupy = df.groupby('Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?')

# Wyświetlenie liczności i statystyk opisowych
print("=== Statystyki liczby wskazanych wad dla każdej grupy poparcia ===")
for nazwa, grupa in grupy:
    print(f"\n{nazwa} (n = {len(grupa)}):")
    print(grupa['Liczba_wad'].describe())

# Przygotowanie danych do testu Kruskala-Wallisa
dane_do_testu = [grupa['Liczba_wad'].values for nazwa, grupa in grupy]

# Test Kruskala-Wallisa
stat, p = kruskal(*dane_do_testu)

print("\n=== Test Kruskala-Wallisa ===")
print(f"Statystyka H = {stat:.3f}")
print(f"p-value = {p:.4f}")
print("----------------------------------------------------------")

# Wykres
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?', y='Liczba_wad', palette='YlGnBu')
plt.title("Liczba dostrzeganych wad a poziom poparcia (test Kruskala-Wallisa)")
plt.xlabel("Poziom poparcia")
plt.ylabel("Liczba wskazanych wad")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

