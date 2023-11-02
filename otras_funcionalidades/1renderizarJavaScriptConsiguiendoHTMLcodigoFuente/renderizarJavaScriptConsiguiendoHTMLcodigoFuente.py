from requests_html import HTMLSession
import os
from bs4 import BeautifulSoup

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

    archivo = open("./sourceCodeAMAZON.txt","w")
    archivo.write(str((html)))
    archivo.close()
    return html



# Ejecución
# La URL corresponde a una búsqueda de "auriculares inalambricos" en AMAZON web
url = "https://www.amazon.es/s?k=auriculares+inalambricos&crid=2Z95CFUYNBBHX&sprefix=auriculares+inalam%2Caps%2C94&ref=nb_sb_ss_ts-doa-p_2_18"
htmlSource = consigueCodigoFuente(url)
