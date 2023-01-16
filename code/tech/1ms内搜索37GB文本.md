#python #杂谈 #tech 

## 文章地址

[Has your password been pwned? Or, how I almost failed to search a 37 GB text file in under 1 millisecond (in Python) - death and gravity](https://death.andgravity.com/pwned)

## 步骤

### 直接搜索

python中使用`sys`逐行读取对应文件
```python

path = sys.argv[1] 
file = open(path, 'rb')

def find_line(lines, prefix): 
	for line in lines: 
		if line.startswith(prefix):
			return line 
		if line > prefix: 
			break 		
	return None
```
虽然可以， 但是目前效率是特别的慢

### hash跳序

假如文件中是有序的，这样我们并不必检查所有行，可以反复跳，直到我们超过了hash的值，然后后退，查看那里的每一行数据

```python
def skip_to_before_line(file, prefix, offset): 
	old_position = file.tell() 
	while True: 
		file.seek(offset, os.SEEK_CUR) 
		file.readline() 
		line = file.readline() 
		# print("jumped to", (line or b'<eof>').decode().rstrip()) 
		if not line or line >= prefix: 
			file.seek(old_position) 
			break 
		old_position = file.tell()
```

### 二叉搜索

 直接通过2分法去逼近文件偏移量。
```python
def skip_to_before_line(file, prefix, offset): 
	while offset > 2**8: 
		offset //= 2 
		skip_to_before_line_linear(file, prefix, offset) 
		
def skip_to_before_line_linear(file, prefix, offset): 
	old_position = file.tell()
```

### 索引

通过构建文件的搜索索引，达到`binary index`的效果