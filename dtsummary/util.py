import json
import chardet

def read_json(path):
    with open(path, 'rb') as f:
        rawdata=f.read()
    encoding = chardet.detect(rawdata)['encoding']
    with open(path, 'r', encoding=encoding) as f:
        result=json.load(f)
    return result

def json_to_cp949(path):
    result = read_json(path)
    with open(path,'w',encoding='cp949') as f:
        json.dump(result,f)
