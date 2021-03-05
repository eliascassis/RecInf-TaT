### Imports
import os
from whoosh import index
from whoosh.qparser import QueryParser,OrGroup
from whoosh.qparser import MultifieldParser
from whoosh.analysis import StemmingAnalyzer

## Function
# Returns db to search
def return_search_index():
    if os.path.exists('news_index_dir'):
        ix = index.open_dir('news_index_dir')
        return ix
    return None

# Searches documents to query
def search(searchText, limit=10, ix=None, textIndex=None, analizer=None):
    if ix is not None:
        if(analizer):
            fixText = ""
            for word in analizer(searchText):
                fixText+=word.text + " "
            searchText = fixText.strip()
        textIndex = textIndex if textIndex else [
            "full_text"
        ]
        global searcher
        searcher = ix.searcher()
        og = OrGroup.factory(0.9)
        parser = MultifieldParser(textIndex, schema=ix.schema, group=og)
        query = parser.parse(searchText)
        results = searcher.search(query, limit=limit)
        return results

# Gets the db
ix = return_search_index()

# Set searcher to query
searcher = None

# Searches for query
results = search(u"lula é acusado de corrupção pela lava jato",ix=ix,analizer=StemmingAnalyzer())

# Fechamento da busca
def searchClose():
    global searcher
    searcher.close()


for result in results:
    print(result)
    print()