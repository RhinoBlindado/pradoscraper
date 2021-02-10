# PRADOscraper
---
![shield](https://img.shields.io/badge/Estado-WIP-red)
## ¿Qué es?
PRADOscraper es un pequeño programa que se encarga de avisar si se ha actualizado un curso que se encuentra en la plataforma MOODLE de la Universidad de Granada, llamado PRADO. Se ha realizado como una _proof of concept_ dado que PRADO nativamente no tiene soporte para notificar cuando se ha añadido o realizado un cambio a algún curso.


## Funcionamiento
PRADOscraper utiliza la herramienta Selenium para automáticamente iniciar sesión en PRADO, una vez dentro, ubica y extrae de cada asignatura su código HTML, el cual se filtra para dejar únicamente los datos legibles por humanos. Estos datos se almacenan y en cada subsecuente ejecución del programa se comparan los cambios entre la versión guardada y la versión nueva del HTML, al final de la ejecución el programa añade el informe detallado de los cambios en el archivo `log.txt`.

_:warning: Esta información está sujeta a cambios a medida que avanza el proyecto._
## Utilización

### Prerequisitos
  * Se debe tener instalado [Selenium junto al geckodriver](https://selenium-python.readthedocs.io/installation.html) para Python.
  
### Instalación y Uso
  1. Clonar el repositiorio.
  2. Dentro de la carpeta `/courses/` se debe tener:
        * `courseList.txt`: Fichero de texto en el que cada línea debe tener **exactamente** el nombre de la asignatura en Prado, una por línea. Se recomienda copiar directamente de Prado el nombre.
        * `loginInfo.txt` : Fichero con la información de inicio de sesión para Prado. En la primera línea el correo, en la segunda la constraseña. **Aún no se está implementada la seguridad, estos datos están en texto plano. Usar con cautela si el equipo es compartido. Se recomienda eliminar permanentemente una vez finalizadas las pruebas**
 3. Iniciar el programa mediante la consola con `python3 /webPrado.py`. Si no hay que añadir más asignaturas, una vez que se completa el paso 1 y 2, solo se debe ejecutar este paso para ver las diferencias.
