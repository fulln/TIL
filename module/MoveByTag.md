
<%*

let li = app.fileManager.vault.fileMap
let fileList = []
let checkDate = tp.file.creation_date("YYYY-MM-DD")
let fileName = tp.file.title

let tags = tp.file.tags()



tags_folder = "daily/"+checkTime +"/" + checkDate

tp.file.move(daily_folder)

%>
