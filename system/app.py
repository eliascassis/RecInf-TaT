### Imports
from flask import Flask, render_template, request
from whoosh_bd.whoosh_search import return_search_index,search,search_close,get_results
from whoosh.analysis import StemmingAnalyzer

# App
app = Flask(__name__)

## Routes
# Index page
@app.route('/')
def index():
    myString = "waiting.html"
    return render_template('index.html',myString=myString)

# Results page
@app.route('/getResultsForQuery',methods=['GET','POST'])
def get_whoosh_documents():
    query = request.form.get("query",False)
    if query:
        query = u"{}".format(query)
        searcher = None
        ix = return_search_index()
        results = search(query,ix=ix,analizer=StemmingAnalyzer())
        if results:
            results = get_results(results)
            myString = 'answers.html'
        else:
            myString = 'invalid_query.html'
        search_close()
        
    else:
        myString = 'waiting.html'
        results = None
    return render_template('index.html',results=results,myString=myString)

# Runs the app
if __name__ == '__main__':
    app.run()
    