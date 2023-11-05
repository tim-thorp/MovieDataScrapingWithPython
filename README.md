# PR1: Web scraping

## Descripción

En este repositorio podrá encontrar los códigos relacionados con la práctica PR1, que se centra en poner en práctica técnicas de Web Scraping, usando Python.
Esta práctica está dentro de la asignatura "Tipología y ciclo de Vida de los Datos", de la UOC. 

El objetivo final de nuestra práctica es conseguir un dataset de películas, con diferentes columnas o atributos de interés, siendo este dataset escrito en un fichero CSV.
Inicialmente se recopian los atributos generales de aproximadamente 1000 películas y el link a cada película; después se usa el link de cada película para recopilar datos concretos de cada película.
Finalmente, se unifican todos los datos recopilados de todas las películas y se escribe el dataset final, en un fichero CSV.

La web de referencia y central de nuestro proyecto es: _https://www.filmaffinity.com/_


## ¿Quiénes realizamos la práctica?

* **Juan Antonio Tora Cánovas** 
* **Tim Thorp**


## ¿Dónde puede encontrar el DATASET?
* **1. En Zenodo:** _https://zenodo.org/records/10072733_
* **2. En DOI.org/:** buscando en _https://www.doi.org/_ por nombre de recurso DOI en la propia web. El recurso será **10.5281/zenodo.10072733**.
* **3. En este repositorio de GitHub:** bajo el directorio "/dataset" desde la raiz de este repositorio, donde tendrá el fichero CSV que sería nuestro dataset.


## DIRECTORIOS
* **/source/main**: aquí se encuentra todo el código fuente de la práctica PR1.
* **/source/otras_funcionalidades**: aquí se encuentra todo el código que, aún quedando fuera de la PR1, ha sido de utilidad para la MEMORIA.PDF o practicar para la PR1.
* **/dataset**: aquí se encuentra el archivo CSV con los datos extraídos.
* **/documentos**: directorio donde puede encontrarse la memoria.pdf y requirements.txt (con info de librerías).


## ARCHIVOS
### -De /source/main-
* **/source/main/main.py**: es el punto de entrada del programa central de la PR1, y el responsable de llamar a otros 2 archivos .py.
* **/source/main/librerias_propias.py**: aquí se encuentran todas las funciones propias, creadas por nosotros durante la PR1. 
* **/source/main/dtos.py**: aquí se define el objeto/clase llamado "ClasePeliculaDTO". Se utilizará como objeto DTO (Data Tansfer Object) en "libreria_funciones_propias.py".
### -De /source/otras_funcionalidades-
* **Los 3 primeros códigos**: creados para probar tiempos y funcionalidades entre Selenium y métodos básicos.
* **Los códigos 4 y 5**: realizados para crear las 2 funciones de raspado de datos que posteriormente se añadieron a la PR1.
* **El código 6**: código para obtener la tecnología del sitio web y los datos del propietario, información útil que se usa en la MEMORIA.PDF.
### -De /dataset-
* **dataset_movie_info.csv**: este archivo corresponde a nuestro dataset generado con nuestro código.
### -De /documentos-
* **Memoria.Rmd**: plantilla codificada en R Markdown.
* **memoria.pdf**: memoria de la práctica PR1 en formato PDF, que es también el PDF resultado de codificar el anterior archivo "Momoria.Rmd".
* **requirements.txt**: fichero txt que incluye todas las librerías instaladas en nuestro PC, entre las que se encuentran las utilizadas en este proyecto.
Las librerías usadas en este proyecto son las siguientes: **requests**, **pandas**, **selenium**, **time**, **csv**, **os**, **builtwith**, **whois** y **lxml**.


## EJECUCIÓN Y USO DEL CÓDIGO
### Código principal
Podrá ejecutarse el código principal desde /source/main/main.py.
Sin parámetros de entrada // Genera como salida el  dataset en formato CSV, en el directorio /dataset.
### Códigos de funcionalidades aisladas
Podrá encontrar 6 archivos de código python en /source/otras:funcionalidades.
Los 3 primeros códigos se utilizaron para probar rendimientos de código básico vs avanzado con Selenium
Los códigos nº 4 y 5 se realizan primero de manera aislada, y luego se añadieron estos en el código principal (o una variante de los mismos).
Por último, el código nº 6 se utiliza para conocer la tecnología y el propietario de la web (información muy útil para decidir el tipo de web scraping que conviene realizar).


## Bibliografía Utilizada
1. Subirats, L., Calvo, M. (2018). *Web Scraping.* Editorial UOC.
2. Lawson, R. (2015). Scraping the Data. En *Web Scraping with Python* (Capítulo 2). Packt Publishing Ltd.
3. Selenium. (2023). *Getting started.* Recuperado de https://www.selenium.dev/documentation/webdriver/getting_started/
