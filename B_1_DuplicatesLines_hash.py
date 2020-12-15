import json
import hashlib

# The name of filename should be replaced accordingly
text_path = 'filename'
json_path = 'summary.json'
duplicate_path =  'dupliacate_lines.txt'
line_number = 0

jsonFile = open(json_path,'w+')
jsonFile.write("{}")
jsonFile.close()


with open(json_path , 'r') as json_file:
    summary = json.load(json_file)  

with open(text_path,'r') as text:
    for line in text:
        line_number += 1
        line = line.rstrip()
        line_hsh = hashlib.md5(line.encode()).hexdigest()
        if line_hsh in summary:
            summary[line_hsh]['repeat'] = int(summary[line_hsh]['repeat']) + 1
            summary[line_hsh]['line_num'].append(line_number)

            with open(json_path,'w') as json_file:
                json.dump(summary, json_file)
            
        else:
            summary[line_hsh] = { "line" : line  ,'repeat' : 1 , 'line_num' : [line_number] }

            with open(json_path,'w') as json_file:
                json.dump(summary, json_file)


with open(json_path) as json_file:
    with open(duplicate_path , 'w+') as duplicate_file:
        summary = json.load(json_file) 
        
        for line, value in summary.items():
            if value['repeat'] > 1:
                duplicate_file.write(value['line']+'\n')

