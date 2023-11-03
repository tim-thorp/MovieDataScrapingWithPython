# PR1: Web scraping

## Descripción

En este repositorio podrá encontrar los códigos relacionados con la práctica PR1, que se centra en poner en práctica técnicas de Web Scraping, usando Python.
Esta práctica está dentro de la asignatura "Tipología y ciclo de Vida de los Datos", de la UOC. 

El objetivo final de la práctica es el de conseguir un DataSet de películas, con diferentes columnas o atributos que consideraremos de interés, siendo este DataSet contenido en un fichero CSV.
Posteriormente, se dirá también atributos tales como: sinapsis, proveedores bajo los que está disponible, etc.

La web de referencia y central de nuestro proyecto es: _https://www.filmaffinity.com/_

## ¿Quiénes realizamos la práctica?

* **Juan Antonio Tora Cánovas** 
* **Tim Thorp**

## Ficheros relevantes de código fuente
### -Directorios clave-
* **src/main**: directorio donde encontramos el código principal de la práctica.
* **src/main**: directorio donde encontramos el código principal de la práctica.
### -Ficheros clave (enumerados de mayor a menor orden de relevancia)-
* **src/main/main.py**: es el punto de entrada del programa central de la PR1, y el responsable de llamar a otros 2 archivos .py.
* **src/main/libreria_funciones_propias.py**: aquí se encuentran todas las funciones propias, creadas por nosotros durante la práctica. 
* **src/main/dtos.py**: aquí se define el objeto/clase llamado "ClasePeliculaDTO". Se utilizará como objeto DTO (Data Tansfer Object) en "libreria_funciones_propias.py".
* **src/otras_funcionalidades/5loginConSelenium.py**: aquí realiza un registro de login simultáneamente en 2 navegadores distintos (Chrome y Firefox).
* **src/otras_funcionalidades/2descargaImagenes.py**: aquí realiza una gestión de recursos audiovisuales, en concreto descarga de imágenes de los productos disponibles de Amazon (bajo cierta búsqueda).

## Bibliografía Utilizada

1. Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
2. Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2.
Scraping the Data
