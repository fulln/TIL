
## 使用

### 复制文件
```shell
scp local_file remote_username@remote_ip:remote_folder 
或者 
scp local_file remote_username@remote_ip:remote_file 
或者 
scp local_file remote_ip:remote_folder 
或者 
scp local_file remote_ip:remote_file
```
### 复制目录
```shell
scp -r local_folder remote_username@remote_ip:remote_folder 
或者 
scp -r local_folder remote_ip:remote_folder
```

### 从远端复制到本地

```shell
scp root@www.runoob.com:/home/root/others/music /home/space/music/1.mp3 
scp -r www.runoob.com:/home/root/others/ /home/space/music/
```

## 注意

如果路径中有空格，则必须使用双反斜杠 \\ 并将整个路径用引号引起来转义字符：
```shell
scp myfile.txt user@192.168.1.100:"/file\\ path\\ with\\ spaces/myfile.txt"
```
