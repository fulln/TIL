#mysql #mysql函数

## 日期函数

### 时间转字符串
```mysql
select date_format(now(), '%Y-%m-%d');  
```
### 时间转时间戳
```mysql
select unix_timestamp(now());
```
‼️ **时间戳长度为10位,即最小单位为s**
### 字符串转时间
```mysql
select str_to_date('2022-12-02', '%Y-%m-%d %H');
```
### 时间戳转时间
```mysql
select from_unixtime(1451997924);
```
### 时间戳转字符串
```mysql
select from_unixtime(1451997924,'%Y-%d');
```

## mysql 时间格式化参数

|值  |含义|  
|---|---|  
|%S、%s|    两位数字形式的秒（ 00,01, ..., 59）|  
|%i|   两位数字形式的分（ 00,01, ..., 59）|  
|%H|   24小时制，两位数形式小时（00,01, ...,23）|  
|%h|   12小时制，两位数形式小时（00,01, ...,12）|  
|%k|   24小时制，数形式小时（0,1, ...,23）|  
|%l|   12小时制，数形式小时（0,1, ...,12）|  
|%T|   24小时制，时间形式（HH:mm:ss）|  
|%r|    12小时制，时间形式（hh:mm:ss AM 或 PM）|  
|%p|   AM上午或PM下午 |  
|%W|   一周中每一天的名称（Sunday,Monday, ...,Saturday）|  
|%a|   一周中每一天名称的缩写（Sun,Mon, ...,Sat） |  
|%w|   以数字形式标识周（0=Sunday,1=Monday, ...,6=Saturday） |  
|%U|   数字表示周数，星期天为周中第一天|  
|%u|   数字表示周数，星期一为周中第一天|  
|%d|   两位数字表示月中天数（01,02, ...,31）|  
|%e|    数字表示月中天数（1,2, ...,31）|  
|%D|   英文后缀表示月中天数（1st,2nd,3rd ...） |  
|%j|   以三位数字表示年中天数（001,002, ...,366） |  
|%M|   英文月名（January,February, ...,December） |  
|%b|   英文缩写月名（Jan,Feb, ...,Dec） |  
|%m|   两位数字表示月份（01,02, ...,12）|  
|%c|   数字表示月份（1,2, ...,12） |  
|%Y|   四位数字表示的年份（2015,2016...）|  
|%y|    两位数字表示的年份（15,16...）|  
|%文字|  直接输出文字内容|