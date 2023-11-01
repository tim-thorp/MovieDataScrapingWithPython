from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
from dtos import ClasePeliculaDTO
import csv



def return_html_after_scrape_movie_info_from_summary_page(browser, num_clics):
    """
    Obtiene el código fuente HTML tras la ejecución de JavaScript y extrae los datos de las películas.
    Parámetros:
        browser: Con los datos de la conexión HTTP establecida y la web cargada.
        num_clics: El número de veces para hacer clic en la flecha para cargar más películas.
                   Por defecto, hacemos clic 33 veces para cargar 1020 películas.
    Return:
        html: El código fuente HTML como una cadena de texto.
    """
    
    
    # Bucle para hacer 33 veces scroll hacia abajo y click en la flecha que con javascrip sigue mostrando más películas
    for i in range(num_clics):
        # Esperamos para evitar sobrecargar el servidor
        time.sleep(3)

        # Hacemos clic en la flecha para cargar más películas
        button = browser.find_element(By.ID, "load-more-bt")
        browser.execute_script("arguments[0].scrollIntoView(true);", button)
        browser.execute_script("arguments[0].click();", button)
    
    # Esperamos para que las últimas 30 películas carguen
    time.sleep(3)
    
    # Obtenemos todo el código fuente HTML de la página con las 1000-1030 películas ya cargadas, incluidos los cambios realizados por JavaScript
    html = browser.page_source
    
    # Cerramos el navegador para liberar recursos
    browser.quit()

    return html





def recoger_detalles_concretos_pelicula_HTML(url, nombre_txt, obj_pelicula):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    html = soup.prettify()

    with open(str(nombre_txt), "w",  encoding="utf-8") as f:
        f.write(html)

    # Consiguiendo valor de "Título original"
    div = soup.find(id="left-column")
    dl  = div.find("dl", class_="movie-info")
    dd = dl.find("dd")
    value = dd.text
    value = value.replace("\t", "")
    value = value.replace(" ", "")
    value = value.replace("\n", "")
    print("Título original: ",value)

     # Consiguiendo valor de "Título original"
    div = soup.find(id="left-column")
    dl  = div.find("dl", class_="movie-info")
    dd = dl.find_all("dd")[2]
    value = dd.text
    print("Duración: ",value)

    # Conseguimos los generos
    #div = soup.find("div", id="left-column")
    #dd  = div.find("dd", _class="card-genres")
    #generos = []
    #for span in dd.findall("span", itemprop="genre"):
    #    a = span.find(a)
    #    value = a.value
    #    generos.append(value)
    #print("Géneros: ", generos)

    # Conseguimos la sinopsis
    sinopsis = soup.find("dd", class_="", itemprop="description")
    value = sinopsis.text
    print("Sinopsis: ", value)




def capture_data_from_sumaryPage(obj_pelicula):
    """
    A partir del HTML extraido, se localizan los datos de interés y se escriben en un fichero CSV.
    Parámetros:
        html: El código fuente en HTML que se extrajo de la web.
    Return:
        obj_detalles_peliculas: objeto de tipo "ClasePeliculasDTO"
    """
    
    # Creamos listas para guardar los valores de cada variable
    movie_titles = []
    movie_years = []
    movie_countries = []
    movie_ratings = []
    movie_rating_counts = []
    movie_directors = []
    movie_cast = []
    movie_links = []
    
    # Analizamos el HTML con lxml
    root = etree.HTML(str(obj_pelicula.get_html()))
    
    # Recopilo datos: recorro todos los div's con la clase "mc-info-container"
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
    
    # Recopilo datos: recorro todos los li's con la clase "data"
    for li in root.xpath('//li[@class="data"]'):
        # Extraemos la puntuación media y el número de puntuaciones
        rating = li.xpath('.//div[@class="avg-rating"]/text()')[0]
        rating_count = li.xpath('.//div[@class="rat-count"]/text()')[0].strip()
        movie_ratings.append(rating)
        movie_rating_counts.append(rating_count)
    
    # Paso los datos recopilados al objeto de retorno
    obj_pelicula.set_movie_titles(movie_titles)
    obj_pelicula.set_movie_years(movie_years)
    obj_pelicula.set_movie_countries(movie_countries)
    obj_pelicula.set_movie_ratings(movie_ratings)
    obj_pelicula.set_movie_rating_counts(movie_rating_counts)
    obj_pelicula.set_movie_directors(movie_directors)
    obj_pelicula.set_movie_cast(movie_cast)
    obj_pelicula.set_movie_links(movie_links)
    return obj_pelicula

def write_data_in_csv(obj_pelicula):

    # Escribimos todo en un archivo CSV
    with open('dataset_movie_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Año', 'País', 'Puntuación Media', 'Número de Puntuaciones', "Director", "Reparto", "Enlace", "Título Original", "Duración", "Género", "Sinopsis"])

        for i, (title, year, country, rating, rating_count, director, cast, link, originalTitle, duration, gender, synopsis) in enumerate(zip(obj_pelicula.get_movie_titles(), 
                                                                                                   obj_pelicula.get_movie_years(), 
                                                                                                   obj_pelicula.get_movie_countries(), 
                                                                                                   obj_pelicula.get_movie_ratings(), 
                                                                                                   obj_pelicula.get_movie_rating_counts(), 
                                                                                                   obj_pelicula.get_movie_directors(), 
                                                                                                   obj_pelicula.get_movie_cast(), 
                                                                                                   obj_pelicula.get_movie_links(), 
                                                                                                   obj_pelicula.get_titulo_original(), 
                                                                                                   obj_pelicula.get_duracion(), 
                                                                                                   obj_pelicula.get_genero(), 
                                                                                                   obj_pelicula.get_sinopsis())
                                                                                                ):
            # Detenemos el proceso si hemos escrito 1000 filas
            if i >= 1000:
                break
            writer.writerow([title, year, country, rating, rating_count, director, cast, link, originalTitle, duration, gender, synopsis])
    


if __name__ == "__main__":
    obj_detalles_peliculas = ClasePeliculaDTO("",[],[],[],[],[],[],[],[],[],[],[],[])
    recoger_detalles_concretos_pelicula_HTML("https://www.filmaffinity.com/es/film893369.html", "fichero.txt", obj_detalles_peliculas)