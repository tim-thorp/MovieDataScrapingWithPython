from selenium import webdriver
from lxml import etree
import csv

def scrape_movie_titles_years_and_countries(url):
    """
    Obtiene el código fuente HTML tras la ejecución de JavaScript y extrae los títulos, años y países de origen de las películas.
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
    
    # Creamos listas para guardar los títulos, años y países de origen de las películas
    movie_titles = []
    movie_years = []
    movie_countries = []
    
    # Recorremos todos los divs con la clase "mc-info-container"
    for div in root.xpath('//div[@class="mc-info-container"]'):
        title_div = div.xpath('.//div[@class="mc-title"]')[0]
        full_text = title_div.xpath('string(.)').strip()
        
        # Obtenemos el título y el año
        title = full_text.split('(')[0].strip()
        year = full_text.split('(')[-1].split(')')[0].strip()
        
        # Obtenemos el país de origen
        country = title_div.xpath('.//img[@class="nflag"]/@alt')[0]
        
        movie_titles.append(title)
        movie_years.append(year)
        movie_countries.append(country)
        
    # Escribimos los títulos, años y países de origen de las películas en un archivo CSV
    with open('movie_titles_years_and_countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Año', 'País'])  # Header
        for title, year, country in zip(movie_titles, movie_years, movie_countries):
            writer.writerow([title, year, country])
    
    return html

# Ejecución
# La URL corresponde a las películas mejores valoradas en Film Affinity (2013–2023)
url = "https://www.filmaffinity.com/es/topgen.php?genres=&chv=0&orderby=avg&movietype=movie%7C&country=&fromyear=2013&toyear=2023&ratingcount=3&runtimemin=0&runtimemax=4"
scrape_movie_titles_years_and_countries(url)
