
<%*

let tags = tp.file.tags
let dirPath = tags.join("/").replaceAll("#","");

dirPath = dirPath + "/" + tp.file.title
tp.file.move(dirPath)

%>
