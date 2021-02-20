### imports
from os import listdir
from os.path import isfile, join

### Auxiliar functions
## Process meta information
def process_meta_information(meta_information=None):
    if meta_information is not None:
        size = len(meta_information)
        for i in range(size):
            meta_information[i] = meta_information[i].replace('\n','')
            meta_information[i] = meta_information[i].replace(',','-')
        return meta_information

## Receives the path o the meta-information directory required for a class (fake or true)
# and returns the csv with the information needed
def join_information(path_dir=None,last_idx=0,label=None):
    if path_dir and label is not None:
        meta_list = [file for file in listdir(path_dir) if isfile(join(path_dir, file))]
        size = len(meta_list)
        counter_idx = last_idx
        out_file = open('../../data/processed_meta_information.csv','a')
        for i in range(size):
            file_meta_information = open(f"{path_dir}/{meta_list[i]}",'r')
            reader_meta_information = file_meta_information.readlines()
            reader_meta_information = process_meta_information(reader_meta_information)
            writed_as_csv_line = f"{counter_idx},{meta_list[i]},{label},{reader_meta_information[1]},{reader_meta_information[2]},{reader_meta_information[3]}"
            for i in range(4,25):
                writed_as_csv_line += f",{reader_meta_information[i]}"
            writed_as_csv_line += '\n'
            counter_idx += 1
            file_meta_information.close()
            out_file.write(writed_as_csv_line)
        out_file.close()
        return counter_idx

# Processing the meta information
last_id = join_information(path_dir='../../data/fake_br/full_texts/fake-meta-information',label='fake')
last_id = join_information(path_dir='../../data/fake_br//full_texts/true-meta-information',label='true',last_idx=last_id)
