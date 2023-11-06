# PR1: Web scraping

## Descripción

En este repositorio encontrará los códigos relacionados con la práctica PR1, centrada en la aplicación de técnicas de Web Scraping usando Python. Esta práctica forma parte de la asignatura "Tipología y ciclo de vida de los datos" de la UOC.

El objetivo final de nuestra práctica es obtener un dataset de películas con diferentes columnas o atributos de interés, el cual se almacena en un fichero CSV. Inicialmente, se recopilan los atributos generales de aproximadamente 1000 películas y el enlace a cada una; después, se utiliza cada enlace para recoger datos específicos. Finalmente, se integran todos los datos recopilados en el dataset final, que se guarda en un fichero CSV.

La web de referencia y central de nuestro proyecto es: _https://www.filmaffinity.com/_

## ¿Quiénes realizamos la práctica?

- **Juan Antonio Tora Cánovas**
- **Tim Thorp**

## ¿Dónde puede encontrar el DATASET?

1. **En Zenodo:** a través del siguiente enlace DOI: _https://doi.org/10.5281/zenodo.10072733_
2. **En este repositorio de GitHub:** bajo el directorio `/dataset` desde la raíz de este repositorio, donde encontrará el fichero CSV correspondiente a nuestro dataset.

## DIRECTORIOS

- **/source/main**: Aquí se encuentra todo el código fuente de la práctica PR1.
- **/source/otras_funcionalidades**: Aquí se encuentra todo el código que, aunque no es parte de la PR1, ha sido útil para la `Memoria.pdf` o para practicar para la PR1.
- **/dataset**: Aquí se encuentra el archivo CSV con los datos extraídos.
- **/documentos**: Directorio donde se pueden encontrar la `Memoria.pdf` y `Requirements.txt` (con información de las librerías).

## ARCHIVOS

### - De /source/main -

- **/source/main/main.py**: Es el punto de entrada del programa central de la PR1, y es responsable de llamar a otros dos archivos .py.
- **/source/main/librerias_propias.py**: Aquí se encuentran todas las funciones propias creadas durante la PR1.
- **/source/main/dtos.py**: Aquí se define el objeto/clase llamado `ClasePeliculaDTO`, que se utiliza como un Data Transfer Object (DTO) en `libreria_funciones_propias.py`.

### - De /source/otras_funcionalidades -

- **Los 3 primeros códigos**: Creados para probar tiempos y funcionalidades entre Selenium y métodos básicos.
- **Los códigos 4 y 5**: Realizados para crear las dos funciones de raspado de datos que posteriormente se incorporaron a la PR1.
- **El código 6**: Utilizado para obtener la tecnología del sitio web y los datos del propietario, información útil para decidir el tipo de web scraping a realizar.

### - De /dataset -

- **dataset_movie_info.csv**: Este archivo corresponde a nuestro dataset generado con nuestro código.

### - De /documentos -

- **Memoria.Rmd**: Plantilla codificada en R Markdown.
- **Memoria.pdf**: Memoria de la práctica PR1 en formato PDF, que es también el resultado de compilar el archivo `Memoria.Rmd`.
- **requirements.txt**: Fichero que incluye todas las librerías instaladas en nuestro PC, entre las cuales se encuentran las utilizadas en este proyecto. Las librerías usadas en este proyecto son: `requests`, `pandas`, `selenium`, `time`, `csv`, `os`, `builtwith`, `whois`, y `lxml`.

## EJECUCIÓN Y USO DEL CÓDIGO

### Código principal

El código principal puede ejecutarse desde `/source/main/main.py`. No requiere parámetros de entrada y genera como salida el dataset en formato CSV, ubicado en el directorio `/dataset`.

### Códigos de funcionalidades aisladas

Se pueden encontrar seis archivos de código Python en `/source/otras_funcionalidades`. Los tres primeros códigos se usaron para probar el rendimiento del código básico versus el avanzado con Selenium. Los códigos nº 4 y 5 se realizaron de manera aislada y, posteriormente, se integraron en el código principal (o una variante de los mismos). Por último, el código nº 6 se utiliza para conocer la tecnología y el propietario de la web, información muy útil para decidir el tipo de web scraping a realizar.

## Bibliografía Utilizada

1. Bristi, W. R., Zaman, Z., & Sultana, N. (2019). Predicting IMDb rating of movies by machine learning techniques. *2019 10th International Conference on Computing, Communication and Networking Technologies (ICCCNT)*, 1-5. IEEE.
2. Creative Commons. (2023). Licencia Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC BY-SA 4.0). Recuperado de https://creativecommons.org/licenses/by-sa/4.0/deed.es
3. Firmanto, A., & Sarno, R. (2018). Prediction of movie sentiment based on reviews and score on Rotten Tomatoes using SentiWordNet. *2018 International Seminar on Application for Technology of Information and Communication*, 202-206. IEEE.
4. Harish, B. S., Kumar, K., & Darshan, H. K. (2019). Sentiment analysis on IMDb movie reviews using hybrid feature extraction method.
5. Lawson, R. (2015). Scraping the Data. En *Web Scraping with Python* (Capítulo 2). Packt Publishing Ltd.
6. Selenium. (2023). Getting started. Recuperado de https://www.selenium.dev/documentation/webdriver/getting_started/
7. Subirats, L., & Calvo, M. (2018). *Web Scraping*. Editorial UOC.