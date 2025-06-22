import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kruskal

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie kolumn
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()
df['Korzyści'] = df['Jakie korzyści dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'].fillna('')
df['Poparcie'] = df['Czy popiera Pan/Pani tworzenie większej liczby łąk miejskich we Wrocławiu?'].str.strip().str.capitalize()

# Filtr: tylko mieszkańcy Wrocławia, kobiety i mężczyźni, bez "Trudno powiedzieć"
df = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna'])) &
    df['Poparcie'].notna() &
    (df['Poparcie'] != 'Trudno powiedzieć')
]


# Lista branych pod uwagę korzyści
dozwolone_korzysci = [
    'Poprawa jakości powietrza',
    'Zwiększenie bioróżnorodności',
    'Miejsce do rekreacji',
    'Poprawa estetyki miasta',
    'Zapobieganie wysokiej temperaturze powietrza'
]

# Przekształcanie kolumny korzyści: licz tylko te z powyższej listy
def licz_korzysci(tekst):
    odpowiedzi = [x.strip() for x in tekst.split(',')]
    return sum(1 for x in odpowiedzi if x in dozwolone_korzysci)

df['Liczba_korzysci'] = df['Korzyści'].apply(licz_korzysci)

# Kategorie odpowiedzi (bez "Trudno powiedzieć")
kategorie = ['Zdecydowanie tak', 'Raczej tak', 'Raczej nie', 'Zdecydowanie nie']
df['Poparcie'] = pd.Categorical(df['Poparcie'], categories=kategorie, ordered=True)


# Statystyki opisowe
print(df.groupby('Poparcie')['Liczba_korzysci'].describe())

# Wykres pudełkowy
plt.figure(figsize=(10, 6))
df.boxplot(column='Liczba_korzysci', by='Poparcie', grid=False, patch_artist=True,
           boxprops=dict(facecolor='lightgreen'))
plt.title("Liczba wybranych (istotnych) korzyści vs poziom poparcia dla łąk miejskich")
plt.suptitle('')
plt.xlabel("Poziom poparcia")
plt.ylabel("Liczba wskazanych korzyści (z 5)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Test Kruskala-Wallisa
groups = [group['Liczba_korzysci'].values for _, group in df.groupby('Poparcie') if not group.empty]
stat, p = kruskal(*groups)
print(f"\nTest Kruskala-Wallisa: statystyka = {stat:.3f}, p-value = {p:.4f}")

if p < 0.05:
    print("➡ Istnieje statystycznie istotna zależność między liczbą wskazanych korzyści a poparciem.")
else:
    print("➡ Brak statystycznie istotnej zależności między liczbą korzyści a poparciem.")

