<%*
let checkDate = tp.file.creation_date("YYYY-MM-DD")
let checkTime = tp.file.creation_date("YYYY-MM")
daily_folder = "daily/"+checkTime+"/"+checkDate
tp.file.move(daily_folder)
%>

<% tp.user.get_date() %>

<% tp.user.get_weather("shenzhen") %>

<% tp.user.get_year_progress() %>


## 每日1题

<% tp.user.leetcode() %>

## 每日单词

| 英文       | 中文       |词根|
| ---------- | ---------- | ---|


## 今日文章

<% tp.user.todayWrite() %>

## 微信阅读

<!-- start of weread -->

<!-- end of weread -->
