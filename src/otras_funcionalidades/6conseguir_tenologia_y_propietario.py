import builtwith
import whois

## Tecnologías usadas ##
tecnologias = builtwith.parse('https://www.filmaffinity.com/es/main.html')
print('LAS TECNOLOGÍAS USADAS POR EL SITIO WEB SON:\n',tecnologias)

## Propietario ##
print('\n \nLA INFO DEL PROPIETARIO DEL SITIO WEB ES:\n',whois.whois('https://www.filmaffinity.com/es/main.html'))