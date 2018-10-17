# Contenedor con Flask

---

# Tabla de Contenido

- [Creacion contenedor con Flask](#creacion-contenedor-con-flask)
- [Exponiendo funciones de Python como Web Services](#exponiendo-funciones-de-python-como-web-services)
- [Creando el primer *endpoint*](#creando-el-primer-endpoint)
- [Recuperando un registro particular](#recuperando-un-registro-particular)
- [Mensajes de error en formato JSON](#mensajes-de-error-en-formato-json)

---

# Creacion contenedor con Flask

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

# Exponiendo funciones de Python como Web Services

Vamos a crear nuestro primer *web service*. 

Observe que ahora nuestro archivo [`gtd.py`](gtd.py) ha cambiado:

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
Aqui el nuevo [`Dockerfile`](Dockerfile).

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

# Creando el primer *endpoint*

Se ha modificado el archivo [`gtd.py`](gtd.py).
En esta modificacion se han adicionado dos elementos:
+ Se crea una lista donde cada nodo de la lista es un diccionario.

```
tasks = [
 {
  'id': 1,
  'title': "Buy groceries",
  'description': "Milk, cheese, pizaa",
  'done': False
 },
 {
  'id': 2,
  'title': "Learn Python",
  'description': "Need a good tutorial on the web",
  'done': False
 }
]
```

+ Se define un nuevo metodo llamado `get_tasks` el cual puede ser accedido a traves del URL [http://localhost:5000/todo/api/v1.0/tasks](http://localhost:5000/todo/api/v1.0/tasks).

```
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
 return jsonify({'tasks': tasks})
```

Observe que el metodo en Python se llama `get_tasks` pero la forma como se accede a este metodo como web service es a traves del URI `/todo/api/v1.0/tasks`.

Usando el comando `curl` tenemos acceso a este nuevo metodo:

```
curl -i http://localhost:5000/todo/api/v1.0/tasks
```

---

# Recuperando un registro particular

Se va a definir un nuevo URI en el cual dado un numero entero el *web service* trae un registro.
A continuacion se presenta el codigo en Python, [`gtd.py`](gtd.py).

```
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
 task = [task for task in tasks if task['id'] == task_id]
 if len(task) == 0:
  abort(404)
 return jsonify({'task': task[0]})
```

Observe que este nuevo metodo se llama `get_task` y recibe como argumento `task_id` el cual se asume sera un numero entero. 
El decorador de este metodo (`@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])`) nos dice que para acceder a este metodo via *web service* el URI es `/todo/api/v1.0/tasks/n` donde `n` debe ser un numero entero.

Lo que hace este metodo es buscar por una tarea que tenga el `task_id` que se paso como argumento a la funcion `get_task`. 
Si se encuentra, se entrega la version JSON de este valor (`return jsonify({'task': task[0]})`).
La razon por la cual se entrega la posicion `0` es porque la instruccion

```
 task = [task for task in tasks if task['id'] == task_id]
```

Devuelve una lista. 
De esa lista respuesta se toma la primera posicion.

En caso que no se encuentre la tarea con el `task_id` se retornara un valor de no encontrado `404`.

## Ejecucion del contenedor

Para ejecutar el contenedor se ejecuta el comando

```
docker run --rm -it -p 5000:5000 -v $(pwd):/myhome josanabr/flask /bin/bash
```

## Accediendo a *web services* via curl

* Trae todas las tareas `curl -i http://localhost:5000/todo/api/v1.0/tasks`
* Trae una tarea en particular `curl -i http://localhost:5000/todo/api/v1.0/tasks/2`
* Trae una tarea inexistente `curl -i http://localhost:5000/todo/api/v1.0/tasks/10`

---

# Mensajes de error en formato JSON

Una buena practica a la hora de desarrollar *web services* es que la forma como exponen sus resultados y sus errores sea a traves del formato JSON. 
Al codigo [`gtd.py`](gtd.py) se adiciono las siguientes instrucciones:

```
@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)
```

Una vez se incorporen estos cambios ejecute el contenedor.
Una vez en el contenedor, ejecute `python3 gtd.py`. 
En otra terminal ejecute el siguiente comando `curl -i http://localhost:5000/todo/api/v1.0/tasks/10`.
Usted deberia ver algo como esto:

> HTTP/1.0 404 NOT FOUND
> Content-Type: application/json
> Content-Length: 27
> Server: Werkzeug/0.14.1 Python/3.6.6
> Date: Wed, 17 Oct 2018 21:32:13 GMT
> 
> {
>   "error": "Not found"
> }

Observe que el error sale ahora en formato JSON.
