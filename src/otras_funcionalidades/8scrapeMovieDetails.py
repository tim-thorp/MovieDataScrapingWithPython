import pandas as pd
import requests
from lxml import html, etree
import time
import csv

def scrape_movie_details(input_csv: str, output_csv: str) -> None:
    """
    Esta función se encarga de extraer detalles específicos de películas a partir de una lista de URLs.
    Los detalles incluyen el título original, la duración, el género y el sinopsis de cada película.
    
    Args:
        input_csv (str): Ruta al archivo CSV que contiene la columna 'Enlace' con las URLs de las películas.
        output_csv (str): Ruta al archivo CSV donde se guardarán los detalles extraídos.
    
    Returns:
        None: La función guarda los detalles directamente en un archivo CSV y no devuelve ningún valor.
    """
    
    # Cargamos el archivo CSV que contiene los enlaces a las páginas de las películas
    df = pd.read_csv(input_csv)
    
    # Convertimos la columna de enlaces en una lista
    url_list = df['Enlace'].tolist()
    
    # Inicializamos listas vacías donde almacenaremos la información extraída
    movie_original_titles = []
    movie_durations = []
    movie_genres = []
    movie_synopses = []
    
    # Iteramos a través de cada URL en la lista
    for i, url in enumerate(url_list):
        print("Extrayendo información de la película {}/{}...".format(i+1, len(url_list)))
        
        # Hacemos una petición GET para obtener el contenido de la página
        response = requests.get(url)
        html_content = response.text
        
        # Utilizamos lxml para analizar el contenido HTML
        root = etree.HTML(html_content)
        
        # Utilizamos xpath para extraer el título original, la duración, el género y el sinopsis
        original_title = root.xpath('.//dt[text()="Título original"]/following-sibling::dd[1]/text()')[0].strip()
        duration = root.xpath('.//dt[text()="Duración"]/following-sibling::dd[1]/text()')[0].split()[0].strip()
        genre = root.xpath('.//dt[text()="Género"]/following-sibling::dd[1]//span[@itemprop="genre"]/a/text()')
        synopsis = root.xpath('.//dt[text()="Sinopsis"]/following-sibling::dd[1]/text()')[0].strip()
        
        # Añadimos la información extraída a las listas correspondientes
        movie_original_titles.append(original_title)
        movie_durations.append(duration)
        movie_genres.append(", ".join(genre))
        movie_synopses.append(synopsis)
        
        # Hacemos una pausa para no sobrecargar el servidor
        time.sleep(3)
    
    # Guardamos la información extraída en un nuevo archivo CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        print("Actualizando {}...".format(output_csv))
        writer = csv.writer(csvfile)
        writer.writerow(['Título Original', 'Duración', 'Género', 'Sinopsis'])
        
        # Escribimos la información fila por fila en el archivo CSV
        for i, (original_title, duration, genre, synopsis) in enumerate(zip(movie_original_titles, movie_durations, movie_genres, movie_synopses)):
            writer.writerow([original_title, duration, genre, synopsis])
            
    print("Extracción completa.")

# Llamamos a la función
scrape_movie_details(input_csv='7movie_info_from_summary_page.csv', output_csv='8movie_details.csv')
