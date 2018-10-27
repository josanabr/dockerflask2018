#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request, send_file

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/")
def saludo():
	return "hola mundo\n"

@app.route("/download/<path>")
def download(path = None):
	print(path)
	if path is None:
		abort(404)
	return send_file(path, as_attachment = True)	

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
