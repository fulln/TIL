"Run this after build_database.py - it needs til.db"
import pathlib
import sqlite_utils
import sys
import re
import json
import os

root = pathlib.Path(__file__).parent.resolve()

index_re = re.compile(r"<!\-\- index starts \-\->.*<!\-\- index ends \-\->", re.DOTALL)
count_re = re.compile(r"<!\-\- count starts \-\->.*<!\-\- count ends \-\->", re.DOTALL)

COUNT_TEMPLATE = "<!-- count starts -->{}<!-- count ends -->"

def download_to_json(context):
    # 准备工作：创建存放json文件夹
    path = "menu.json"
    '''
    用于JSON文件下载
    '''
    with open(path, 'w', encoding='utf-8') as result:
        json.dump(context, result, ensure_ascii=False)


def merge_values(val1, val2):
    if val1 is None:
        return val2
    elif val2 is None:
        return val1
    else:
        if val1.__contains__("value") & val2.__contains__("value"):
            return [val1, val2]
        else:
            return get_huge_dict(val1,val2)

def get_huge_dict(val1, val2):
    return {
            key:merge_values(val1.get(key),val2.get(key))
            for key in set(val1).union(val2)
        }

def findOrSave(row,entity):
    if len(row) >5:
        row=row[:5]
    current_dict={}
    row_index = len(row)
    for i in range(1,row_index + 1):
        if current_dict == {}:
            current_dict[row[row_index -i]] ={"value":entity} 
        else:
            new_dict = {}
            new_dict[row[row_index -i]] =current_dict     
            current_dict =new_dict
    return current_dict        

def glance_line(total_dict,sharp,line):
    for key, value in total_dict.items():
        if value is None:
            continue    
        if type(value).__name__=='dict' :
            if key == 'value':
                thisline = "* [{title}]({url}) - {date}".format(
                    date=value["created"].split("T")[0], **value
                )
                line.append(thisline)        
            else:
                line.append("{} {}\n".format(sharp,key))
                glance_line(value,sharp+"#",line)      
        elif type(value).__name__=='list':
            line.append("{} {}\n".format(sharp,key))           
            for i in range(len(value)):     
                glance_line(value[i],sharp+"#",line)

if __name__ == "__main__":
    db = sqlite_utils.Database(root / "til.db")
    
    index = ["<!-- index starts -->"]
    total_dict = {}
    
    for row in db["til"].rows_where(order_by="created_utc"):
        topic = json.loads(str(row["topic"])
        print(row)                   
        current_dict = findOrSave(row, i)
        total_dict =get_huge_dict(current_dict,total_dict)
                        
    glance_line(total_dict,"##",index)
    if index[-1] == "":
        index.pop()
    index.append("<!-- index ends -->")
    
    
    zs_json= {}
    for row in db["til"].rows_where(order_by="created_utc desc limit 5"):
         zs = "* [{title}]({url}) - {date}".format(
                    date=row["created"].split("T")[0], **row
                )
         zs_json.setdefault("top",[]).append(zs)   
    download_to_json(zs_json)
    
    if "--rewrite" in sys.argv:
        readme = root / "README.md"
        index_txt = "\n".join(index).strip()
        readme_contents = readme.open().read()
        rewritten = index_re.sub(index_txt, readme_contents)
        table = db.table("til", pk="path")
        rewritten = count_re.sub(COUNT_TEMPLATE.format(table.count), rewritten)
        readme.open("w").write(rewritten)
    else:
        print("\n".join(index))
