
# Imports
from flask import Flask, render_template, request, json,send_file
from pandas import read_json
import os

# Caminho absoluto do arquivo de saída
path = os.path.relpath("files/pseudoPalavras.xlsx")

# App
app = Flask(__name__)

## Routes
# Página inicial
@app.route('/')
def index():
    myString = 'form_words.html'
    return render_template('index.html',myString=myString)

# Exibe a lista de palavras encontradas
@app.route('/getResultsForQuery',methods=['GET','POST'])
def get_whoosh_documents():
    print()

# Roda a aplicação
if __name__ == '__main__':
    app.run(debug=True)