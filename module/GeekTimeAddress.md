<%*

let date = new Date(); 
let month = date.getMonth()+1;
let d = date.getDate();

tp.date.now("yyyy-MM")
tp.file.move(daily_folder)

return "此文章为"+month+"月day"+d+" 学习笔记，内容来源于极客时间《》"
%>