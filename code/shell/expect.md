#脚本 #shell #自动化流程
## shell 脚本流程控制以及登录

要想实现一键shell脚本登录,需要用到的是``expect`这个包`

#### 下载

mac上下载

```shell
brew install expect
```

#### 使用

由于是shell脚本，虽然网上说是用tcl语言来编写的这个脚本，但是还是比较方便易用的

主要使用由以下4个主要流程
 
- 赋值 set
- 执行 spawn 
- 匹配 expect
- 反馈 send

具体的使用不做分析了，网上有很多的demo，下面贴下登录的脚本

```shell
#!/usr/bin/expect 
set ipaddress [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
set locations [lindex $argv 3]
if { $argc != 4 } {
puts "Usage: expect login.exp ipaddress username password"
exit 1
}
set timeout 30
spawn ssh $username@$ipaddress
expect {
        "(yes/no)" {send "yes\r"; exp_continue}
        "password:" {send "$password\r"}
}
expect "$username@*"  {send "cd /app/applogs/$locations/\r"}
interact
```

这个是单抽出来的登录用的expect脚本，可以和我[另外写的shell脚本](https://github.com/fulln/sampleScrips/tree/master/ssh_script)联合使用进行登录
