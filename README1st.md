# Solucion a problema en clase

# Presunciones

Para ejecutar correctamente este [`Dockerfile`](Dockerfile) es necesario tener una imagen de Docker que tenga ya instalado Flask.
A continuacion el contenido del `Dockerfile`

```
FROM josanabr/flask
COPY gtd.py /myhome/gtd.py
ENTRYPOINT [ "python3" ]
CMD [ "/myhome/gtd.py" ]
```

Se copia el [`gtd.py`](gtd.py) dentro de la imagen del contenedor.
Se establece que el comando a ejecutarse en este contenedor es el comando `python3`.
Se pasa como argumento al `python3` el script que tiene el *web service*

# Construir la imagen

Para construir la imagen se ejecuta el siguiente comando

```
docker build -t josanabr/flask:1.0.1 .
```

# Ejecutar la nueva imagen

```
docker run --rm -d -p 5000:5000 josanabr/flask:1.0.1
```

# Otra ejecucion

```
docker run --rm -it -p 5000:5000 -v $(pwd):/myhome --name flask josanabr/flask /bin/bash
```
