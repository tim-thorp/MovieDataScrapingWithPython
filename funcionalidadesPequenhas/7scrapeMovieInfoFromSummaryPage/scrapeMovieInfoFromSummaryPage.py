from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
import csv

def scrape_movie_info_from_summary_page(url, num_clics=33):
    """
    Obtiene el código fuente HTML tras la ejecución de JavaScript y extrae los datos de las películas.
    Parámetros:
        url: La URL a buscar.
        num_clics: El número de veces para hacer clic en la flecha para cargar más películas.
                   Por defecto, hacemos clic 33 veces para cargar 1020 películas.
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
    
    # Esperamos para que la página cargue
    time.sleep(3)
    
    # Buscamos el botón «ACEPTO» y lo clicamos
    button = browser.find_element(By.CLASS_NAME, "css-v43ltw")
    button.click()
    
    for i in range(num_clics):
        # Esperamos para evitar sobrecargar el servidor
        time.sleep(3)

        # Hacemos clic en la flecha para cargar más películas
        button = browser.find_element(By.ID, "load-more-bt")
        browser.execute_script("arguments[0].scrollIntoView(true);", button)
        browser.execute_script("arguments[0].click();", button)
    
    # Esperamos para que las últimas 30 películas carguen
    time.sleep(3)
    
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
    movie_directors = []
    movie_cast = []
    movie_links = []
    
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
        
        # Obtenemos el director y el reparto
        director = div.xpath('.//div[@class="mc-director"]/div[@class="credits"]/span/a/text()')
        cast = div.xpath('.//div[@class="mc-cast"]/div[@class="credits"]/span/a/text()')
        
        # Obtenemos el enlace de la película
        link = div.xpath('.//div[@class="mc-title"]/a/@href')[0]
        
        movie_titles.append(title)
        movie_years.append(year)
        movie_countries.append(country)
        movie_directors.append(", ".join(director))
        movie_cast.append(", ".join(cast))
        movie_links.append(link)
        
    # Recorremos todos los lis con la clase "data"
    for li in root.xpath('//li[@class="data"]'):
        # Extraemos la puntuación media y el número de puntuaciones
        rating = li.xpath('.//div[@class="avg-rating"]/text()')[0]
        rating_count = li.xpath('.//div[@class="rat-count"]/text()')[0].strip()
        
        movie_ratings.append(rating)
        movie_rating_counts.append(rating_count)
    
    # Escribimos todo en un archivo CSV
    with open('movie_info_from_summary_page.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Año', 'País', 'Puntuación Media', 'Número de Puntuaciones', "Director", "Reparto", "Enlace"])

        for i, (title, year, country, rating, rating_count, director, cast, link) in enumerate(zip(movie_titles, movie_years, movie_countries, movie_ratings, movie_rating_counts, movie_directors, movie_cast, movie_links)):
            # Detenemos el proceso si hemos escrito 1000 filas
            if i >= 1000:
                break
            writer.writerow([title, year, country, rating, rating_count, director, cast, link])

    return html

# Ejecución
url = "https://www.filmaffinity.com/es/topgen.php?genres=&chv=0&orderby=avg&movietype=movie%7C&country=&fromyear=2013&toyear=2023&ratingcount=3&runtimemin=0&runtimemax=4"
scrape_movie_info_from_summary_page(url)
