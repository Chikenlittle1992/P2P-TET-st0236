# info de la materia: ST263 <Tópicos Especiales en Telemática>
#
# Estudiante(s): 
# Miguel Angel Escudero Colonia, maescuderc@eafit.edu.co
# Esneider Zapata Arias, ezapataa1@eafit.edu.co
#
# Profesor: Juan Carlos Montoya Mendoza, jcmontoy@eafit.edu.co
#

# Reto N1. Aplicaciones P2P
#
# 1. Breve descripción de la actividad

Se desarrolló una aplicación que permite la transferencia de archivos simulada con una arquitectura P2P estructurada haciendo uso de DHT

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- Conexión entre nodos
- Comunicación entre peers usando gRPC
- "Subir" archivos a la red
- Encontrar archivos en la red
- Cada nodo tiene su Hash Table de archivos que puede ser consultada por los demás nodos

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- Conexión y desconexión correcta de nodos (Todos los nodos son vecinos de todos, no se maneja la desconexión)

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

- Lenguaje de Programación: Python 3.12
- Librerias: grpcio 1.66.1, grpcio-tools 1.66.1

## Como se compila y ejecuta.

1. Clonar el repositorio: `git clone https://github.com/Chikenlittle1992/P2P-TET-st0236.git`
2. Abrir una terminal y acceder a la carpeta donde se clonó el repo
3. Pararse en la rama "test1" `git checkout test1`
4. Instalar librerias necesarias `pip install -r requirements.txt`
5. Para probar las funcionalidades, ejecute `py start_node.py`
6. Ingrese localhost y un puerto disponible (ejemplo `localhost:5001`)
7. Deje el siguiente campo vacio ya que es el primer peer en unirse a la red
8. Abra una nueva terminal y ejecute `py start_node.py` de nuevo, escriba un nuevo port `localhost:5002`
9. En el campo del nodo bootstrap ingrese el primer nodo que conectó a la red (en este caso `localhost:5001`)
10. Puede conectar más nodos, y probar las funcionalidades de subir archivos y buscarlos

## detalles del desarrollo.
## detalles técnicos
## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor.

## una mini guia de como un usuario utilizaría el software o la aplicación

# 5. otra información que considere relevante para esta actividad.

# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-url 
## sitio2-url
## url de donde tomo info para desarrollar este proyecto
