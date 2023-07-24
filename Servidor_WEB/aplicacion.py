from flask import Flask,render_template,request

pagina = Flask(__name__)

@pagina.route('/')
def funcion():
    return render_template('primera_pagina.html')

if __name__ == '__main__':
    pagina.run(debug=True)