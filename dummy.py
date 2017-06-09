from flask import Flask, render_template, request, jsonify, json
import requests
import traceback
import os

app = Flask(__name__)


@app.route('/documents', methods=['GET'])
def get_docs():
    print("Obteniendo documentos")
    return 'Obtencion correcta de documentos'

@app.route('/search', methods=['POST'])
def handle_num_doc():
    print("Obteniendo DNI")
	
    return "Pasando el numero de doc al metodo que obtendra el documento, para ser adjuntado"

if __name__ == "__main__":
    app.run(debug=True, port=3000)

