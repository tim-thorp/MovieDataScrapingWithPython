from selenium import webdriver
from lxml import etree
import csv

def scrape_movie_data_from_summary_page(url):
    """
    Obtiene el código fuente HTML tras la ejecución de JavaScript y extrae los datos de las películas.
    Parámetros:
        url: La URL a buscar.
    Devoluciones:
        html: El código fuente HTML como una cadena de texto.
    """
    
    # Abrimos el navegador Firefox en modo headless
    options = webdriver.FirefoxOptions()
    options.headless = True
    
    # Creamos una nueva instancia del navegador Firefox con las opciones definidas
    browser = webdriver.Firefox(options=options)
    
    # Navegamos a la URL especificada
    browser.get(url)
    
    # Obtenemos el código fuente HTML de la página, incluidos los cambios realizados por JavaScript
    html = browser.page_source
    
    # Cerramos el navegador para liberar recursos
    browser.quit()
    
    # Analizamos el HTML con lxml
    root = etree.HTML(html)
    
    # Creamos listas para guardar los valores de cada variable
    movie_titles = []
    movie_years = []
    movie_countries = []
    movie_ratings = []
    movie_rating_counts = []
    
    # Recorremos todos los divs con la clase "mc-info-container"
    for div in root.xpath('//div[@class="mc-info-container"]'):
        title_div = div.xpath('.//div[@class="mc-title"]')[0]
        full_text = title_div.xpath('string(.)').strip()
        
        # Obtenemos el título y el año
        title, year = full_text.rsplit('(', 1)
        year = year.rstrip(')')
        title = title.strip()
        
        # Obtenemos el país de origen
        country = title_div.xpath('.//img[@class="nflag"]/@alt')[0]
        
        movie_titles.append(title)
        movie_years.append(year)
        movie_countries.append(country)
        
    # Recorremos todos los lis con la clase "data"
    for li in root.xpath('//li[@class="data"]'):
        # Extraemos la puntuación media y el número de puntuaciones
        rating = li.xpath('.//div[@class="avg-rating"]/text()')[0]
        rating_count = li.xpath('.//div[@class="rat-count"]/text()')[0]
        
        movie_ratings.append(rating)
        movie_rating_counts.append(rating_count)
    
    # Escribimos todo en un archivo CSV
    with open('movie_titles_years_countries_ratings.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Año', 'País', 'Puntuación Media', 'Número de Puntuaciones'])
        for title, year, country, rating, rating_count in zip(movie_titles, movie_years, movie_countries, movie_ratings, movie_rating_counts):
            writer.writerow([title, year, country, rating, rating_count])
    
    return html

# Ejecución
# La URL corresponde a las películas mejores valoradas en Film Affinity (2013–2023)
url = "https://www.filmaffinity.com/es/topgen.php?genres=&chv=0&orderby=avg&movietype=movie%7C&country=&fromyear=2013&toyear=2023&ratingcount=3&runtimemin=0&runtimemax=4"
scrape_movie_data_from_summary_page(url)
