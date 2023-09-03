---
dg-publish: true
tags:
  - 日志
createTime: <% tp.file.creation_date() %>
---
<%*
let checkDate = tp.file.creation_date("YYYY-MM-DD")
let checkTime = tp.file.creation_date("YYYY-MM")
daily_folder = "daily/"+checkTime+"/"+checkDate
await tp.file.move(daily_folder)
%>

<% tp.user.get_date() %>

<% tp.user.get_weather("shenzhen") %>

<% tp.user.get_year_progress() %>

## 体重摄入

### 昨日体重： 73.5
### 今日计划

| 类别           | 参数                    |
| -------------- | ----------------------- |
| 日期           | <% tp.date.now() %>               |
| 锻炼消耗卡路里 | |
| 目标           | 60      （7500千卡为消耗1KG）                |
| 目前剩余次数               |        225                  |



## 每日1题


## 每日单词

| 英文       | 中文       |词根|
| ---------- | ---------- | ---|


## 今日文章
 <%*
let li = app.fileManager.vault.fileMap
let fileList = []

getChildren(li["code"].children,fileList)
getChildren(li["lib"].children,fileList)

function getChildren(list,fileList){  
   list.forEach(e => {  
       if (e.children) {  
           getChildren(e.children,fileList)  
       }else{       
		    if(moment(e.stat.ctime).format("YYYY-MM-DD") == checkDate){
			    fileList.push(e)
		    }
       }  
   })  
}

fileList = fileList.map(f => {
    return "- [["+f.name+"]]\n"
})
fileList = fileList.join("")
%>
<% fileList %>
## 微信阅读

<!-- start of weread -->

<!-- end of weread -->
