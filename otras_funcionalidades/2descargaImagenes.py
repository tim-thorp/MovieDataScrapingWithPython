
import requests
from requests_html import HTMLSession
import os
from bs4 import BeautifulSoup


def descargar_imagenes_contenidas_en_html_source(html):
    """
    Descarga todas las imágenes que hay en el HTML renderizado.
    Params:
        html: el código fuente con el html renderizado
    Returns:
        imagenes: Diccionario de imágenes descargadas.
    """

    # Obtiene todas las etiquetas <img> del código HTML
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all('div', class_='a-section aok-relative s-image-square-aspect')

    imgs = []
    for div in divs:
        imgActual = div.find("img")
        imgs.append(imgActual)

    # Crea el directorio de imagenes descargas
    if not os.path.exists("imagenesProductos/"):
        os.mkdir("imagenesProductos/")

    # Descarga y guarda las imágenes
    imagenes = {}
    i=0
    for img in imgs:
        src = img["src"]
        filename = str(i)+".jpg"
        with open("imagenesProductos/" + filename, "wb") as f:
            f.write(requests.get(src).content)
        imagenes[filename] = src
        i+=1
    # Creo fichero para guardar lista de imagenes descargadas
    archivo = open("imagenesProductos/" + "registroImgsDescargas.txt", "w")
    archivo.write(str((imagenes)))
    archivo.close()
    
    return imagenes



def consigueCodigoFuente(url):
    """
    Consigue el HTML de código fuente de un sitio web, tras renderizar el JavaScript.
        Params:
            url: La URL del sitio web
        Returns:
            html: Código fuente en HTML tras renderizar el JavaScript
    """
    session =HTMLSession()
    resp = session.get(url)
    resp.html.render()
    soup = BeautifulSoup(resp.html.html, "html.parser")
    html =soup.prettify()
    return html



if __name__ == "__main__":
    # Ejecución
    url = "https://www.amazon.es/s?k=auriculares+inalambricos&crid=2Z95CFUYNBBHX&sprefix=auriculares+inalam%2Caps%2C94&ref=nb_sb_ss_ts-doa-p_2_18"
    htmlSource = consigueCodigoFuente(url)
    descargar_imagenes_contenidas_en_html_source(htmlSource)
