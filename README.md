# Create Secure Password - CSP
![Logo](./img/logo.png)

## Index
- [El Desafío De Las Contraseñas](#el-desafío-de-las-contraseñas)
    - [El Handicap De Las Contraseñas](#el-handicap-de-las-contraseñas)
    - [Método Para Crear Contraseñas Robustas](#método-para-crear-contraseñas-robustas)
- [Instalación](#instalacion)
- [Uso de la Herramienta](#uso-de-la-herramienta)
    - [Arguments Mode](#arguments-mode)
    - [Interactive Mode](#interactive-mode)

## El Desafío De Las Contraseñas

### El Handicap De Las Contraseñas

Recordar contraseñas puede resultar complicado, especialmente al cumplir con las medidas recomendadas, como tener una cuenta nueva para cada servicio, contraseñas distintas, una longitud adecuada, caracteres especiales, números, mayúsculas y minúsculas, entre otros requisitos.

En la actualidad, la necesidad de crear cuentas para diversos propósitos hace prácticamente imposible recordar todas estas contraseñas. Las soluciones convencionales, como el uso de un administrador de contraseñas (que a menudo implica una suscripción de pago) o apuntarlas en una libreta, son válidas pero pueden no resultar ideales.

Personalmente, estas opciones no parecen ser las mejores alternativas. ¿Y si solo necesitáramos recordar una frase relacionada con la cuenta y luego fortalecerla para crear una contraseña sólida y fácil de recordar?

Es con esta premisa que nace el proyecto Create Secure Password (CSP). Ofrece una nueva perspectiva para la creación y gestión de contraseñas, permitiéndote recordar una única frase y transformarla en contraseñas robustas para cada cuenta.

### Método Para Crear Contraseñas Robustas

Imaginemos que tengamos que crear una cuenta en cualquier plataforma, como GitHub. El primer paso sería crear una frase que nos recuerde fácilmente a este sitio, puede ser un comentario gracioso, una referencia al servicio que ofrece, etc. el caso es que sea una frase que tú dirías.

Posteriormente tendrías que fortificar esa frase creándole una serie de normas, poner palabras en mayúsculas, utilizar signos, números, etc. en mi caso, mi lógica me lleva a este pensamiento:

`github promotes open source more or less -> G1th()bPr0m0t3$0P3n$0()rc3M0r30RL3$$`

Lo que hacemos es que a algunas letras les añadimos una asociación a un número o a un carácter, además de hacer que cada palabra de la frase tenga una mayúscula, cumpliendo con los requisitos de complejidad.

Ahora lo que podemos hacer es almacenar simplemente las frases y realizarles esta conversión, las frases por sí solas no tienen sentido y si alguien las leyería, pensarían que simplemente estás loco.

Es cierto que es muy tedioso hacer esto manualmente, pero CSP lo hará por ti =)

## Instalacion

### Requisitos
El único requisito es tener instalado en el sistema la versión 3.12 o superior de python.

### Creación De Un Ejecutable Manualmente

En lo personal, no encuentro cómodo tener que descargar y mantener en mi entorno de Python varias librerías, ya que esto puede dificultar el proceso de desarrollo. Mi preferencia es crear un archivo ejecutable que contenga tanto la lógica del programa como todas las dependencias necesarias, simplificando así el entorno de desarrollo y permitiéndome centrarme en la programación sin preocuparme por la gestión individual de bibliotecas.

Por este motivo, prefiero utilizar herramientas como PyInstaller. Al generar un archivo ejecutable, consigo no solo una distribución más sencilla del programa, sino también la capacidad de construir mi propio conjunto de ejecutables personalizados y almacenarlos path específico, para no tener que añadir comando inecesarios a la hora de ejecutar dichas herramientas. 


### Utilización Desde Python

## Uso de la Herramienta
Create Secure Password (CSP) es una herramienta de línea de comandos diseñada para convertir frases en contraseñas. Aunque esta herramienta está enfocada para usuarios que saben utilizar una línea de comandos a nivel básico, también implementa una forma interactiva que facilita la creación y ofrece una experiencia amigable para el usuario.

### Arguments Mode

En el caso de que queramos agilizar el proceso de creación de la contraseña podemos utilizar los argumentos predefinidos, para verlos simplemente tendremos que ejecutar el comando con el flag --help o no indicar ningún argumento.
``` bash
csp --help
```
![help_menu](./img/help_menu.png)

ejemplo de uso:

``` bash
csp -p 'cookies steal information from us' -s ' '
```
![args_mode](./img/args_mode.png)

### interactive mode

podemos habilitar el modo interactivo utilizando el argumento '-i' a la hora de ejecutar la herramienta. ej:
``` bash
csp -i
```
![interactive_mode](./img/interactive_mode.png)