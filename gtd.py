#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

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

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
 return jsonify({'tasks': tasks})

@app.route('/')
def saludo():
	return "hola mundo"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
