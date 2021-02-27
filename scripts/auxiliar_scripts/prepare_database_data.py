### Imports
from pandas import read_csv,read_json

# Reading csv file ../../data/predicted_news_data.csv
meta_file = read_csv('../../data/predicted_news_data.csv')

# Selecting the required data
news_text_list = []
for index, row in meta_file.iterrows():
    index_at_directory = row['index at directory'].split('-')
    label = 'true' if row['label'] else 'fake'
    directory_path = f"../../data/fake_br/full_texts/{label}/{index_at_directory[0]}.txt"
    file = open(directory_path,'r')
    meta_file.loc[meta_file.index[row['index']], 'full text'] = file.read()
    file.close()

# Exporting to json
meta_file.to_json('../../data/json_whoosh_analysis.json')
file_test = read_json('../../data/json_whoosh_analysis.json')
print(file_test.head(10))