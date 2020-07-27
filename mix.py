from datetime import timezone
import git
import pathlib

root = pathlib.Path(__file__).parent.resolve()

table = []

def created_changed_times(repo_path, ref="master"):
    created_changed_times = {}
    repo = git.Repo(repo_path, odbt=git.GitDB)
    commits = reversed(list(repo.iter_commits(ref)))
    for commit in commits:
        dt = commit.committed_datetime
        affected_files = list(commit.stats.files.keys())
        for filepath in affected_files:
            if filepath not in created_changed_times:
                created_changed_times[filepath] = {
                    "created": dt.isoformat(),
                    "created_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            created_changed_times[filepath].update(
                {
                    "updated": dt.isoformat(),
                    "updated_utc": dt.astimezone(timezone.utc).isoformat(),
                }
            )
    return created_changed_times


def build_list(repo_path):
    all_times = created_changed_times(repo_path)
    for filepath in root.glob("*/*.md"):
        fp = filepath.open()
        title = fp.readline().lstrip("#").strip()
        body = fp.read().strip()
        path = str(filepath.relative_to(root))
        url = "https://github.com/fulln/TIL/blob/master/{}".format(path)
        record = {
            "path": path.replace("/", "_"),
            "topic": path.split("/"),
            "title": title,
            "url": url,
            "body": body,
        }
        record.update(all_times[path])
        table.append(record)


index_re = re.compile(r"<!\-\- index starts \-\->.*<!\-\- index ends \-\->", re.DOTALL)
count_re = re.compile(r"<!\-\- count starts \-\->.*<!\-\- count ends \-\->", re.DOTALL)

COUNT_TEMPLATE = "<!-- count starts -->{}<!-- count ends -->"

if __name__ == "__main__":
    build_list(root)   
    db = sqlite_utils.Database(root / "til.db")
    by_topic = {}
    for row in db["til"].rows_where(order_by="created_utc"):
        by_topic.setdefault(row["topic"], []).append(row)
    index = ["<!-- index starts -->"]
    for topic, rows in by_topic.items():
        sharp = '##'
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
        print("\n".join(index))if __name__ == "__main__":
    
