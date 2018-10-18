# Contenedor con Flask

---

# Tabla de Contenido

- [Creacion contenedor con Flask](#creacion-contenedor-con-flask)
- [Exponiendo funciones de Python como Web Services](#exponiendo-funciones-de-python-como-web-services)
- [Creando el primer *endpoint*](#creando-el-primer-endpoint)
- [Recuperando un registro particular](#recuperando-un-registro-particular)
- [Mensajes de error en formato JSON](#mensajes-de-error-en-formato-json)
- [Adicionando una tarea via POST](#adicionando-una-tarea-via-post)
- [Actualizando y borrando tareas](#actualizando-y-borrando-tareas)
- [Palabras finales](#palabras-finales)

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

---

# Adicionando una tarea via POST

Hasta ahora lo que se ha hecho es acceder a la lista de tareas que se encuentran almacenadas en memoria del *web service*. 
En este punto lo que se va a hacer es ingresar una nueva tarea que se almacenara en la memoria del *web service*. 
El metodo que permite esta funcionalidad es el siguiente:

```
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
 if not request.json or not 'title' in request.json:
  abort(400)
 task = {
  'id': tasks[-1]['id'] + 1,
  'title': request.json['title'],
  'description': request.json.get('description', ""),
  'done': False
 }
 tasks.append(task)
 return jsonify({'task': task}), 201
```

Observe que el URI para acceder a este servicio que crea una tarea es `/todo/api/v1.0/tasks`, el cual es similar al URI que hemos visto anteriormente.
La gran diferencia es el metodo que se usa para acceder al *web service*, en este caso es el metodo `POST`. 

Una vez el cliente hace un llamado `POST` al URI `/todo/api/v1.0/tasks` se invoca el metodo `create_task()`.
Si la solicitud no es de tipo JSON se aborta la solicitud.
De lo contrario, se crea una nueva tarea. 
Se adiciona a la lista de tareas existentes y se retorna la tarea en formato JSON y con un codigo `201`, creado.

Para probar el nuevo archivo,

* Ejecutar el contenedor
* Una vez en el contenedor ejecute el comando `python3 gtd.py`
* Por fuera del contenedor ejecutar el siguiente comando

```
curl -i -H "Content-Type: application/json" -X POST -d '{"title": "read a book"}' http://localhost:5000/todo/api/v1.0/tasks
```

* Liste ahora las tareas que tiene almacenadas en memoria el `web service`

---

# Actualizando y borrando tareas

A continuacion se presentan dos metodos, un metodo que permite la actualizacion de los datos de una tarea y un metodo que permite borrar tareas.
A continuacion se presenta la implementacion del metodo para actualizar los datos de una tarea:

```
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})
```

La funcion `delete_task`, como los anteriores, tiene un decorador que apunta al URI `/todo/api/v1.0/tasks/n` (donde `n` se espera sea un numero entero) pero esta vez usa el metodo `PUT` del protocolo HTTP. 
Ademas de recibir el identificador de la tarea a actualizar, este metodo espera recibir un JSON donde se describiran que informacion sera la que se actualice. 
Una vez se valida que todo esta en orden, se procede a actualizar la tarea que el usuario indico se debe actualizaar.

Ahora, observemos la implementacion del *web service* que permite borrar una tarea. 

```
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
```

Esta funcion en Python tiene el mismo URI (`/todo/api/v1.0/tasks/n`) pero el metodo del protocolo HTTP que usa es el `DELETE`.
Lo que hace la funcion `delete_task` entonces es localizar la tarea y una vez encontrada la remueve de la lista. 

## Interactuando con los nuevos metodos

### Ejecucion de los *web services*

* Arrancar el contenedor `docker run --rm -it -p 5000:5000 -v $(pwd):/myhome josanabr/flask /bin/bash` 
* Una vez dentro del contenedor, ejecutar el comando `python3 gtd.py`

### Accediendo a los *web services* via `curl`

En esta oportunidad interactuaremos con los *web services* de dos formas, una para actualizar y otra para eliminar.
Para actualizar se ejecuta lo siguiente:

```
curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2
```

Ahora liste las tareas que estan en memoria para validar que se hizo el cambio del *status* de la tarea.

Ahora se procedera con el borrado de tareas. 
Digite usted mismo los comandos.

---

# Palabras finales

* Observe que todos los *web services* que se definieron tenian el mismo URI, `/todo/api/v1.0/tasks`
* A pesar de ser usado el mismo URI, el *web server* direcciona a una funcion en Python o a otra dependiendo del metodo HTTP que se haya escogido
* A traves del comando `curl` es posible interactuar con *web services* y enviar informacion en formato JSON
* Flask es un micro-framework que facilita enormemente el desarrollo de *web services*
