import pandas as pd
import regex as re
import random as rd

def buscarPelicula(df, pelicula_inicial):
    lista_peliculas = df['name'].tolist()
    lista_elegidas = []

    for i in range(len(lista_peliculas)):
        pattern = re.compile(pelicula_inicial, re.IGNORECASE)
        if re.findall(pattern, lista_peliculas[i]) != []:
            lista_elegidas.append(lista_peliculas[i])
    try:
        pelicula = rd.choice(lista_elegidas)
        indice_pelicula = lista_peliculas.index(pelicula)
    except:
        indice_pelicula = -1

    return indice_pelicula

def recomendador(df, df_pelicula):
    lista_recomendadas = []

    # Recomendamos peliculas que tengan el mismo genero
    for i in range(len(df)):
        if df['genre'][i] == df_pelicula['genre'] and df['name'][i] != df_pelicula['name']:
            lista_recomendadas.append(df.iloc[i])
    
    # Recomendamos peliculas que sean del mismo director
    for i in range(len(df)):
        if df['director'][i] == df_pelicula['director'] and df['name'][i] != df_pelicula['name']:
            lista_recomendadas.append(df.iloc[i])
        
    # Recomendamos peliculas que tengan el mismo actor estrella
    for i in range(len(df)):
        if df['star'][i] == df_pelicula['star'] and df['name'][i] != df_pelicula['name']:
            lista_recomendadas.append(df.iloc[i])

    # El recomendador añade a una lista las peliculas del mismo genero, director y actor estrella
    # y las ordena de mejor puntuadas a peor. Luego, elige una aleatoria entre las 10 mejores recomendadas
    lista_recomendadas.sort(key=lambda x: x['score'], reverse=True)

    return lista_recomendadas


def etl(nombre_archivo):
    # Esta funcion se encarga de extraer, transformar y cargar los datos para
    # analizarlos y recomendar peliculas

    # Extraemos los datos
    df = pd.read_csv(nombre_archivo)


    # Transformamos los datos:
    #   Eliminamos las columnas que no nos interesan
    df.drop([
        'rating', 'released', 'votes', 
        'writer', 'country', 'budget', 
        'gross', 'runtime'
            ], axis=1, inplace=True)

    #   Eliminamos las filas que tengan valores nulos
    df.dropna()


    # Cargamos los datos para usarlos en el modelo
    return df



def main():
    df = etl('movies.csv')

    pelicula_inicial = input("Escribe el nombre de una pelicula: ")
    indice_pelicula = buscarPelicula(df, pelicula_inicial)
    while indice_pelicula == -1:
        pelicula_inicial = input("La pelicula no se encuentra en el dataframe. Escribe el nombre de una pelicula: ")
        indice_pelicula = buscarPelicula(df, pelicula_inicial)
    
    df_pelicula = df.iloc[indice_pelicula]

    lista_recomendadas = recomendador(df, df_pelicula)
    mejores_recomendaciones = lista_recomendadas[0:10]

    pelicula_recomendada = rd.choice(mejores_recomendaciones)

    print(f"Pelicula elegida: \n{df_pelicula}\n\n")
    print(f"Pelicula recomendada: \n{pelicula_recomendada}\n\n")

    
    return



if __name__ == "__main__":
    main()