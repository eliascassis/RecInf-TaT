### Imports
import os
from whoosh import index
from whoosh.qparser import OrGroup
from whoosh.qparser import MultifieldParser

## Function
# Returns db to search
def return_search_index():
    if os.path.exists('./whoosh_bd/news_index_dir'):
        ix = index.open_dir('./whoosh_bd/news_index_dir')
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

# Fechamento da busca
def search_close():
    global searcher
    searcher.close()

# Splits results in lists of fake and true observing falsity score
def split_falsity(results_list=None,r=10):
    if results_list is not None:
        aux_fake = []
        aux_true = []
        for i in range(r):
            if results_list[i]['falsity'] > .2: 
                aux_fake.append(results_list[i])
            else:
                aux_true.append(results_list[i])
        return (aux_true,aux_fake)

# Format results in a DataFrame and return the sorted documents
def get_results(results_list):
    results = [dict(hit) for hit in results_list]
    results = split_falsity(results)
    results_true = [true_hit for true_hit in results[0]]
    results_fake = [fake_hit for fake_hit in results[1]]
    results_fake.sort(key=lambda x: x['veracity'], reverse=True)
    merged_results = []
    for result in results_true:
        merged_results.append(result)
    for result in results_fake:
        merged_results.append(result)
    return merged_results