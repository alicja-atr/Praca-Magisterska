import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie kolumn
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()

# Filtrowanie tylko mieszkańców Wrocławia z podaną płcią
df = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Płeć'].isin(['Kobieta', 'Mężczyzna']))
]

# Czyszczenie kolumny korzyści
df['Korzyści'] = df['Jakie korzyści dostrzega Pan/Pani w istnieniu łąk miejskich? (można zaznaczyć wiele odpowiedzi)'].fillna('').str.strip()

# Rozdzielanie odpowiedzi
df['Korzyści_lista'] = df['Korzyści'].str.split(',')

# Spłaszczanie i czyszczenie
all_answers = df['Korzyści_lista'].explode().str.strip().str.lower()

# Lista akceptowanych odpowiedzi
dozwolone_korzysci = [
    'poprawa jakości powietrza',
    'zwiększenie bioróżnorodności',
    'miejsce do rekreacji',
    'poprawa estetyki miasta',
    'zapobieganie wysokiej temperaturze powietrza',
    'nie dostrzegam korzyści'
]

# Filtrowanie
filtered = all_answers[all_answers.isin(dozwolone_korzysci)]

# Liczenie częstości i sortowanie malejąco
answer_counts = filtered.value_counts().sort_values(ascending=False)

# Wykres
plt.figure(figsize=(10,6))
bars = answer_counts.plot(kind='bar', color='skyblue')

# Dodanie liczby wskazań na słupkach
for i, value in enumerate(answer_counts):
    plt.text(i, value + 0.5, str(value), ha='center', va='bottom', fontsize=9)

plt.title("Częstość wyboru wybranych korzyści z istnienia łąk miejskich")
plt.xlabel("Korzyść")
plt.ylabel("Liczba wskazań")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

