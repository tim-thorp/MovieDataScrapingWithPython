from selenium import webdriver
from lxml import etree
import csv

def scrape_movie_titles_and_years(url):
    """
    Obtiene el código fuente HTML tras la ejecución de JavaScript y extrae los títulos y años de las películas.
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
    
    # Creamos listas para guardar los títulos y años de las películas
    movie_titles = []
    movie_years = []
    
    # Recorremos todos los divs con la clase "mc-title"
    for div in root.xpath('//div[@class="mc-title"]'):
        full_text = div.xpath('string(.)').strip()
        title = full_text.split('(')[0].strip()
        year = full_text.split('(')[-1].split(')')[0].strip()
        
        movie_titles.append(title)
        movie_years.append(year)
        
    # Escribimos los títulos y años de las películas en un archivo CSV
    with open('movie_titles_and_years.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Año'])  # Header
        for title, year in zip(movie_titles, movie_years):
            writer.writerow([title, year])
    
    return html
