
<%*

let checkDate = tp.file.creation_date("YYYY-MM-DD")
let checkTime = tp.file.creation_date("YYYY-MM")

daily_folder = "daily/"+checkTime +"/" + checkDate

tp.file.move(daily_folder)

%>
