#python #pip

## 国内相关pipy源

	1. 清华大学：https://pypi.tuna.tsinghua.edu.cn/simple/
	2. 阿里云：http://mirrors.aliyun.com/pypi/simple/
	3. 豆瓣：http://pypi.douban.com/simple/ 

## 临时使用

我们可以直接在 pip 命令中使用 -i 参数来指定镜像地址，例如：

```python
pip install -i http://pypi.douban.com/simple/ numpy
pip install -i http://pypi.douban.com/simple/--trusted-host pypi.douban.com  

## 此参数"--trusted-host"表示信任，如果上一个提示不受信任，就使用这个
```

## 永久使用

### 创建**pip.conf** 文件

```bash
cd ~/.pip
touch pip.conf
```

然后写入对应内容

```conf
[global] 
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn 
```

然后保存退出即可。
