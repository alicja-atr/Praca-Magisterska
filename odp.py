import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("ankieta.csv", encoding='utf-8')

# Czyszczenie podstawowe
df['Płeć'] = df['Płeć'].str.strip().str.capitalize()
df['Wiek'] = df['Wiek'].str.strip()
df['Wykształcenie'] = df['Wykształcenie'].str.strip().str.capitalize()
df['Status zawodowy'] = df['Status zawodowy'].str.strip().str.capitalize()
df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] = df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'].str.strip().str.capitalize()
df['Czy wie Pan/Pani czym są łąki miejskie?'] = df['Czy wie Pan/Pani czym są łąki miejskie?'].str.strip().str.capitalize()

# Filtr próby badawczej: mieszkańcy Wrocławia + wiedza o łąkach
df_filtered = df[
    (df['Czy jest Pan/Pani mieszkańcem/mieszkanką Wrocławia?'] == 'Tak') &
    (df['Czy wie Pan/Pani czym są łąki miejskie?'] == 'Tak')
]

# Ustawienie kolejności kategorii
df_filtered['Płeć'] = pd.Categorical(df_filtered['Płeć'], categories=[
    'Kobieta', 'Mężczyzna', 'Inna', 'Wolę nie podawać'], ordered=True)

df_filtered['Wykształcenie'] = pd.Categorical(df_filtered['Wykształcenie'], categories=[
    'Średnie', 'Wyższe', 'Zasadnicze zawodowe', 'Wolę nie podawać'], ordered=True)

df_filtered['Status zawodowy'] = pd.Categorical(df_filtered['Status zawodowy'], categories=[
    'Uczeń/student', 'Pracujący', 'Bezrobotny', 'Emeryt/rencista', 'Inne', 'Wolę nie podawać'], ordered=True)

# Funkcja do wykresów
def analiza_demograficzna(df, kolumna, tytul):
    rozklad = df[kolumna].value_counts().sort_index()
    print(f"\nRozkład odpowiedzi dla {kolumna}:")
    print(rozklad)
    
    plt.figure(figsize=(8,5))
    rozklad.plot(kind='bar', color='cornflowerblue')
    plt.title(tytul)
    plt.ylabel("Liczba odpowiedzi")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# Informacja o liczbie odpowiedzi
print("Liczba odpowiedzi po filtracji:", len(df_filtered))

# Wykresy demograficzne
analiza_demograficzna(df_filtered, 'Płeć', 'Rozkład płci respondentów ankiety')
analiza_demograficzna(df_filtered, 'Wiek', 'Rozkład wieku respondentów ankiety')
analiza_demograficzna(df_filtered, 'Wykształcenie', 'Rozkład wykształcenia respondentów ankiety')
analiza_demograficzna(df_filtered, 'Status zawodowy', 'Rozkład statusu zawodowego respondentów ankiety')

