from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
import csv
from dtos import ClasePeliculaDTO
from libreria_funciones_propias import return_html_after_scrape_movie_info_from_summary_page, recoger_detalles_concretos_pelicula_HTML, capture_data_from_sumaryPage, write_data_in_csv
from threading import Thread
import requests
from bs4 import BeautifulSoup


def capture_details_from_all_filmPage(obj_pelicula):
    
    links = obj_pelicula.get_movie_links()
    titulo_original = obj_pelicula.get_titulo_original()
    duracion = obj_pelicula.get_duracion()
    genero = obj_pelicula.get_genero()
    sinopsis = obj_pelicula.get_sinopsis()
    print("Recopilando datos de película específica, de la 0 a la 1029...")

    for i in range(len(links)):
        response = requests.get(links[i])
        soup = BeautifulSoup(response.content, "html.parser")
        html = soup.prettify()

        try:
            # Consiguiendo valor de "Título original"
            div = soup.find(id="left-column")
            dl  = div.find("dl", class_="movie-info")
            dd = dl.find("dd")
            value = dd.text
            value = value.replace("\t", "")
            value = value.replace(" ", "")
            value = value.replace("\n", "")
            titulo_original.append(value)
        except Exception as e:
            titulo_original.append("")

        try:
            # Consiguiendo valor de "Título original"
            div = soup.find(id="left-column")
            dl  = div.find("dl", class_="movie-info")
            dd = dl.find_all("dd")[2]
            value = dd.text
            duracion.append(value)
        except Exception as e:
            duracion.append("")

        try:
            # Conseguimos los generos
            #div = soup.find("div", id="left-column")
            #dd  = div.find("dd", _class="card-genres")
            #generos = []
            #for span in dd.findall("span", itemprop="genre"):
            #    a = span.find(a)
            #    value = a.value
            #    generos.append(value)
            #print("Géneros: ", generos)
            genero.append("")
        except Exception as e:
            genero.append("")

        try:   
            # Conseguimos la sinopsis
            elementoHtml = soup.find("dd", class_="", itemprop="description")
            value = elementoHtml.text
            sinopsis.append(value)
            print(i)
        except Exception as e:
            sinopsis.append("")
            print(i)
        finally:
            time.sleep(3)
        
    obj_pelicula.set_titulo_original(titulo_original)
    obj_pelicula.set_duracion(duracion)
    obj_pelicula.set_genero(genero)
    obj_pelicula.set_sinopsis(sinopsis)
    return obj_pelicula






################## Ejecución ###################
# tiempo inicial
t0 = time.perf_counter_ns()

# inicializo objetos de pelicula y web
url = "https://www.filmaffinity.com/"
obj_detalles_peliculas = ClasePeliculaDTO("",[],[],[],[],[],[],[],[],[],[],[],[])

# Abrir navegador Firefox y acceder a URL general
options = webdriver.FirefoxOptions()
options.headless = True

# Instanciamos navegador Firefox con opciones definidas y navegamos a la URL deseada
browser = webdriver.Firefox(options=options)
browser.get(url)
time.sleep(5)

# Buscamos el botón «ACEPTO» y lo clicamos
button = browser.find_element(By.CLASS_NAME, "css-v43ltw")
button.click()

# navegación a la sección "TopFA"
irTopFA = browser.find_element(By.XPATH, '/html/body/header/div[2]/div/ul/li[1]/a').click()
time.sleep(3)

# Cargo la página "TopFA" con filtro de búsqueda concreto
browser.get("https://www.filmaffinity.com/es/topgen.php?genres=&chv=0&orderby=avg&movietype=movie%7C&country=&fromyear=2013&toyear=2023&ratingcount=3&runtimemin=0&runtimemax=4")

# realizo raspado inicial y guardo html devuelto
html = return_html_after_scrape_movie_info_from_summary_page(browser, 33)
obj_detalles_peliculas.set_html(html)

# Tomo instantes de tiempo después del raspado inicial
t1 = time.perf_counter_ns()
tiempo_raspando_inicial = (t1 - t0) / 10**9

# Recopilamos los datos del sumaryPage
obj_detalles_peliculas = capture_data_from_sumaryPage(obj_detalles_peliculas)
print("El tiempo que tardamos en raspar todos los datos generales es de: ",tiempo_raspando_inicial," (segundos)")

# Recopilamos los datos detallados de cada película
obj_detalles_peliculas = capture_details_from_all_filmPage(obj_detalles_peliculas)

# Creación del DATASET
write_data_in_csv(obj_detalles_peliculas)

# Tomamos tiempos midiento retardos escribiendo DATASET (csv)
t2 = time.perf_counter_ns()
tiempo_escribiendo_csv = (t2 - t1) / 10**9

# Imprimo información de los costes temporales por consola
print("El tiempo que tardamos en volcar los datos raspados a fichero CSV: ",tiempo_escribiendo_csv," (segundos)")


