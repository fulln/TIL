---
dg-publish: true
title: dirname使用过程
createTime: 2023-12-05 18:00
tags:
  - shell
  - linux
---
## dirname 用处

`dirname` 是一个标准的计算机程序，通常在 Unix 和类 Unix 操作系统中使用。当 `dirname` 命令接收到一个路径名时，它会删除任何以最后一个斜杠（'/'）字符开始的后缀，并返回结果。这个命令通常在 shell 脚本中使用。`dirname` 命令的使用方法是给定一个路径名，然后它会返回该路径名的目录部分。例如，`dirname` 命令可以从路径名中提取目录路径名，忽略任何尾随斜杠。

