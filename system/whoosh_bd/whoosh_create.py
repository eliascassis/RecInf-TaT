### Imports 
from pandas import read_json
import os
from shutil import rmtree
from whoosh.index import create_in
from whoosh.fields import NUMERIC,TEXT,Schema
from whoosh.analysis import StemmingAnalyzer

### Functions
## Function to create the db
def createDB(db_name,schema):
    if os.path.exists(db_name):
        rmtree(db_name)
    os.mkdir(db_name)
    ix = create_in(db_name, schema)
    return ix

## Registers the docs
def registerDocs(ix,documents):
    writer = ix.writer()
    for index, row in documents.iterrows():
        writer.add_document(index=row['index'], link=row['link'], category=row['category'], date=row['date of publication'], veracity=row['veracity'], label=row['label'], full_text=u"{}".format(row['full text']))
    writer.commit()
    return getDocCount(ix)

## Count registered docs
def getDocCount(ix):
    searcher = ix.searcher()
    docsLength = searcher.doc_count()
    searcher.close()    
    return docsLength

# db name
db_name = "news_index_dir"

# Defines the schema
schema = Schema(index=NUMERIC(stored=True),
                link=TEXT(analyzer=None,stored=True),
                category=TEXT(analyzer=None,stored=True),
                date=TEXT(analyzer=None,stored=True),
                veracity=NUMERIC(stored=True),
                label=NUMERIC(stored=True),
                full_text=TEXT(analyzer=StemmingAnalyzer(stoplist=None),stored=True))

# Creates the db
ix = createDB(db_name,schema)

# Reads the data
data = read_json('../../data/json_whoosh_analysis.json')

# Registers the documents
docs_length = registerDocs(ix, data)
print(f"OK! The {docs_length} documents was registered!")