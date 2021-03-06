# Imports
from flask import Flask, render_template, request, json,send_file
from pandas import read_json
# import os
from whoosh_bd.whoosh_search import return_search_index,search,search_close,get_results
from whoosh.analysis import StemmingAnalyzer


def before_request():
    app.jinja_env.cache = {}
# App
app = Flask(__name__)

## Routes
# Página inicial
@app.route('/')
def index():
    myString = "null.html"
    return render_template('index.html',myString=myString)

# Exibe a lista de palavras encontradas
@app.route('/getResultsForQuery',methods=['GET','POST'])
def get_whoosh_documents():
    query = request.form.get("query",False)
    query = u"{}".format(query)
    searcher = None
    ix = return_search_index()
    results = search(query,ix=ix,analizer=StemmingAnalyzer())
    results = get_results(results)
    search_close()
    with open('templates/answers.html','w') as html:
        for index,row in results.iterrows():  
            category = row['category']
            link = row['link']
            falsity = 'danger' if row['falsity'] > .2 else 'success'
            short_text = f"{row['full_text']}"
            news_size = 500#int(len(short_text) * .25)
            short_text = f"{short_text[:news_size]}..."
            date = row['date']
            html.write('<p></p>\n')
            html.write(f'<div class="card text-center border-{falsity} mb-3" style="width:60%">\n')
            html.write(f'    <div class="card-header border-{falsity}">\n')
            html.write(f'       {category}\n')
            html.write('    </div>\n')
            html.write('    <div class="card-body">\n')
            html.write(f'        <p class="card-text">{short_text}</p>\n')
            html.write('    </div>\n')
            html.write('    <div class="card-body">\n')
            html.write(f'        <a href="{link}" class="card-link">veja a notícia na íntegra</a>\n')
            html.write('    </div>\n')
            html.write(f'   <div class="card-footer border-{falsity}" >\n')
            html.write(f'       {date}\n')
            html.write('    </div>\n')
            html.write('</div>\n')        

    myString = 'answers.html'
    return render_template('index.html',myString=myString)

# Roda a aplicação
if __name__ == '__main__':
    app.run()
    