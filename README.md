Backend Din Express
===
# Tabla de contenidos

- [Backend de Din Express](https://github.com/eldeivid420/AdelantosNomina)
- [Tabla de contenidos](#tabla-de-contenidos)
  - [Información del código](#información-del-código-a-name--abouta)
  - [Jerarquía de directorios](#jerarquía-de-directorios)
  - [Iniciar el proyecto](#iniciar-el-proyectoa-name--gettingstarteda)
  - [Archivo de variables de entorno](#archivo-de-variables-de-entorno-env)
  - [Entorno de ejecución virtual](#entorno-virtual-de-ejecición-a-name--venva)

## Información del código <a name = "about"></a>
- Title: `Backend de Din Express`
- Authors: `David Rodriguez Fragoso`
- Lenguaje: `Python 3.11`
- Framework `Flask`

## Jerarquía de directorios
El proyecto se organiza de la siguiente forma:

```
|—— Global
|   |── Classes
|       |── Adelanto.py
|       |── Auth.py
|       |── Empleado.py
|       |── Gerente.py
|       |── Operador.py
|       |── Ticket.py
|   |── Controllers
|       |── Adelanto.py
|       |── Auth.py
|       |── Empleado.py
|       |── Gerente.py
|       |── Operador.py
|       |── Ticket.py
|   |── Routes
|       |── Auth.py
|       |── Gerente.py
|       |── Incoming.py
|       |── Operador.py
|   |── Utils
|       |── db.py
|── venv_app
|   |── bin
|   |── lib
|   |── pyenv.cfg
|── .env
|── ADELANTOS_NOMINA_DDL.txt
|── LICENSE
|── main
|── requirements.txt
|── run.py
|── wsgi.py
```
Para saber más del archivo .env, consultar [Archivo de variables de entorno (.env)](#archivo-de-variables-de-entorno-env).
Dentro de la carpeta `/Global/Classes` tenemos las clases implementadas en el proyecto.
```
|── Classes
|   |── Adelanto.py
|   |── Auth.py
|   |── Empleado.py
|   |── Gerente.py
|   |── Operador.py
|   |── Ticket.py
```
* El archivo `Adelanto.py` contine la clase encargada de hacer las operaciones CRUD que tengan que ver con adelantos.
* El archivo `Auth.py` contine la clase encargada de hacer las validaciones de seguridad necesarias.
* El archivo `Empleado.py` contine la clase encargada de hacer las operaciones CRUD que tengan que ver con empleados.
* El archivo `Gerente.py` contine la clase encargada de hacer las operaciones CRUD que tengan que ver con gerentes.
* El archivo `Operador.py` contine la clase encargada de hacer las operaciones CRUD que tengan que ver con operadores.
* El archivo `Tickets.py` contine la clase encargada de hacer las operaciones CRUD que tengan que ver con quejas y sugerencias.

Dentro de la carpeta `/Global/Controllers` tenemos los controladores de las clases.
```
|── Controllers
|   |── Adelanto.py
|   |── Auth.py
|   |── Empleado.py
|   |── Gerente.py
|   |── Operador.py
|   |── Ticket.py
```
* El archivo `Adelanto.py` es el encargado de mandar a llamar los métodos necesarios para realizar una operación relacionada con adelantos.
* El archivo `Auth.py` es el encargado de mandar a llamar los métodos necesarios para realizar una operación relacionada con validaciones de seguridad.
* El archivo `Empleado.py` es el encargado de mandar a llamar los métodos necesarios para realizar una operación relacionada con empleados.
* El archivo `Gerente.py` es el encargado de mandar a llamar los métodos necesarios para realizar una operación relacionada con gerentes.
* El archivo `Operadores.py` es el encargado de mandar a llamar los métodos necesarios para realizar una operación relacionada con operadores.
* El archivo `Ticket.py` es el encargado de mandar a llamar los métodos necesarios para realizar una operación relacionada con quejas y sugerencias.

Dentro de la carpeta `/Global/Routes` tenemos las rutas disponibles.
```
|── Routes
|   |── Auth.py
|   |── Gerente.py
|   |── Incoming.py
|   |── Operador.py
```
* El archivo `Auth.py` contiene las rutas disponibles para realizar validaciones de seguridad.
* El archivo `Gerente.py` contiene las rutas disponibles para un perfil de tipo "gerente".
* El archivo `Incoming.py` es el encargado de definir y llamar los controladores necesarios para una solicitud del bot de Din Express.
* El archivo `Operador.py` contiene las rutas disponibles para un perfil de tipo "gerente".

Dentro de la carpeta `/Global/Utils` están las confifguraciones adicionales para algunas dependencias
```
|── Utils
|   |── db.py
```
Dentro del archivo `db.py` se crea la conexión a la base de datos y se declaran los request GET y POST

Dentro de la carpeta `/venv_app` tenemos el entorno de ejecución virtual del proyecto. <a name = "venv"></a>
```
|── venv_app
|   |── bin
|   |── lib
|   |── pyenv.cfg
```
Para más información, acceder al apartado [entorno virtual de ejecución](#entorno-virtual-de-ejecición-a-name--venva)

Dentro del archivo `main.py` se encuentran las configuraciones iniciales de la aplicación y es el archivo ejecutable principal.
```
|── main.py
```
Dentro del archivo `requirements.txt` se encuentran las dependencias necesarias para ejecutar el proyecto

Dentro del archivo `run.py` se encuentra la configuración para ejecutar la aplicación en modo producción.

Dentro del archivo `wsgi.py` se encuentra la configuración para ejecutar la aplicación desde gunicorn

## Iniciar el proyecto<a name = "getting_started"></a>
Lo primero que hay que hacer es clonar este repositorio, después hay que completar los siguientes pasos:
### Archivo de variables de entorno (.env)
Es necesario crear un archivo de variables de entorno con las siguientes configuraciones:
```
# DB CONFIG

DB_NAME = [el nombre de tu base de datos]
DB_USER = [el usuario de tu base de datos]
DB_PASSWORD = [el password de tu base de datos]
DB_HOST = '127.0.0.1' o bien [ipv4 de tu servidor]
DB_PORT = [el puerto de tu base de datos]

# FLASK CONFIG

FLASK_PORT = [tu puerto de flask]
JWT_TOKEN = "[tu token de JWT]"

# TWILIO CONFIG

ACCOUNT_SID = '[tu SID de Twilio]'
AUTH_TOKEN = '[tu token de autenticación de Twilio]'
```
### Entorno virtual de ejecición <a name = "venv"></a>
* Para ejectutar el entorno virtual, es necesario seleccionarlo en el IDE como intérprete
* En caso de estar en consola, ejectutar el ejecutable `bin/activate`
* Una vez realizado esto, hay que instalar las dependencias necesarias con el comando `pip install -r requirements.txt`

Una vez creado el archivo de configuración y seleccionado un entorno de ejecución de Python3.11, hay que ejecutar el archivo `run.py`.
En caso de estar haciendo uso de gunicorn, entonces el archivo a ejecutar será el archivo `wsgi.py`
