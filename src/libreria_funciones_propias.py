from requests_html import HTMLSession
import requests
import os
from bs4 import BeautifulSoup

def consigueCodigoFuente_si_noHTML(url):
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

    nombre_archivo = url.replace("https://","")
    nombre_archivo = nombre_archivo.replace("/", "-")
    nombre_archivo = nombre_archivo.replace(".", "_")
    archivo = open("",nombre_archivo,".txt","w")
    archivo.write(str((html)))
    archivo.close()
    return html


def captura_detalle_pelicula_HTML(url, nombre_txt):
    response = requests.get(url)
    html = BeautifulSoup(response.content, "html.parser")

    with open(str(nombre_txt), "w") as f:
        for dd in html.find_all("dd", class_="", itemprop="description"):
            print(dd.text)
            f.write(str(dd.text))
    
    

if __name__ == "__main__":
    captura_detalle_pelicula_HTML("https://www.filmaffinity.com/es/film893369.html", "fichero.txt")