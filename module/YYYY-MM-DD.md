<%*
let checkDate = tp.file.creation_date("YYYY-MM-DD")
let checkTime = tp.file.creation_date("YYYY-MM")
daily_folder = "daily/"+checkTime+"/"+checkDate
tp.file.move(daily_folder)
%>

<% tp.user.get_date() %>

<% tp.user.get_weather("shenzhen") %>

<% tp.user.get_year_progress() %>

## 体重摄入

### 上周体重： 75
### 本周体重
| 类别           | 参数                    |
| -------------- | ----------------------- |
| 日期           | <% tp.date.now() %>               |
| 锻炼           |               |
| 摄入           |  |
| 锻炼消耗卡路里 | |
| 体重           |  76                      |
| 目标           | 60      （7500千卡为消耗1KG）                |
| 目前需要天数               |                          |



## 每日1题


## 每日单词

| 英文       | 中文       |词根|
| ---------- | ---------- | ---|


## 今日文章

<% tp.user.todayWrite() %>

## 微信阅读

<!-- start of weread -->

<!-- end of weread -->
