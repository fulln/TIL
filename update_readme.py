"Run this after build_database.py - it needs til.db"
import pathlib
import sqlite_utils
import sys
import re
import json

root = pathlib.Path(__file__).parent.resolve()

index_re = re.compile(r"<!\-\- index starts \-\->.*<!\-\- index ends \-\->", re.DOTALL)
count_re = re.compile(r"<!\-\- count starts \-\->.*<!\-\- count ends \-\->", re.DOTALL)

COUNT_TEMPLATE = "<!-- count starts -->{}<!-- count ends -->"

def download_to_json(topic):
    # 准备工作：创建存放json文件夹
    path = "menu.json"
    '''
    用于JSON文件下载
    '''
    if not os.path.exists(path):
        os.system(r"touch {}".format(path))  # 调用系统命令行来创建文件
    with open(path, 'w', encoding='utf-8') as result:
        json.dump(context, result, ensure_ascii=False)




if __name__ == "__main__":
    db = sqlite_utils.Database(root / "til.db")
    by_topic = {}
    for row in db["til"].rows_where(order_by="created_utc"):
        by_topic.setdefault(str(row["topic"]), []).append(row)
    index = ["<!-- index starts -->"]
    for topic, rows in by_topic.items():
        sharp = '##'
        topic = json.loads(topic)
        for i in range(len(topic)):
            index.append("{} {}\n".format(sharp,topic[i]))
            sharp = sharp +'#'
        for row in rows:
            index.append(
                "* [{title}]({url}) - {date}".format(
                    date=row["created"].split("T")[0], **row
                )
            )
        index.append("")
    download_to_json(by_topic)    
    if index[-1] == "":
        index.pop()
    index.append("<!-- index ends -->")
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
