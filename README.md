# Contenedor con Flask

Inicialmente, se aprovisionara un contenedor con Flask. 

```
docker build -t josanabr/flask .
```

La imagen resultado de ejecutar este contenedor se puede ejecutar de forma interactiva como sigue:

```
docker run --rm -it -P -v $(pwd):/myhome josanabr/flask /bin/bash
```

De acuerdo a esta ejecucion el **directorio** desde donde se ejecuta este contenedor sera expuesto dentro del contenedor en el directorio `/myhome`.

Estando dentro del contenedor, ingrese al directorio `/myhome` y ejecute:

```
python3 gtd.py
```

Deberia obtener el famoso `hola mundo`.

---

Vamos a crear nuestro primer *web service*. 

Observe que ahora nuestro archivo [gtd.py](gtd.py) ha cambiado:

```
#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

@app.route('/')
def saludo():
	return "hola mundo"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
```

Para llevar a cabo un poco mas automatica la ejecucion de este contenedor tambien se alterara un poco la definicion de nuestro contenedor. 
Aqui el nuevo `Dockerfile`.

```
FROM ubuntu
RUN apt-get update
RUN apt-get -y --fix-missing install python3-pip ; exit 0
RUN pip3 install Flask
EXPOSE 5000
WORKDIR /myhome
```

Modificamos la ejecucion anterior del contenedor:

```
docker run --rm -it -p 5000:5000 -v $(pwd):/myhome josanabr/flask /bin/bash
```

Estando dentro del contenedor se ejecuta:

```
python3 gtd.py
```

Abra otra terminal e ingrese a la maquina donde se esta ejecutando el contenedor. 
Ejecute el comando:

```
curl -i http://localhost:5000
```

Ahora se tiene un servidor web que responde con `hola mundo`.

---

Se ha modificado el archivo [gtd.py](gtd.py).
En esta modificacion se ha creado una lista donde cada nodo de la lista es un diccionario.
Asi mismo se define un nuevo metodo llamado `get_tasks` el cual puede ser accedido a traves del URL [http://localhost:5000/todo/api/v1.0/tasks](http://localhost:5000/todo/api/v1.0/tasks).

Usando el comando `curl` tenemos acceso a este nuevo metodo:

```
curl -i http://localhost:5000/todo/api/v1.0/tasks
```
