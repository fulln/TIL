---
dg-publish: true
tags:
  - markdown
  - "#流程图"
createTime: 2023-01-27 12:49
---
## 概念

-   什么是Mermaid？
	- Mermaid是一种基于Javascript的绘图工具，使用类似于Markdown的语法，使用户可以方便快捷地通过代码创建图表。
	- 项目地址：[https://github.com/mermaid-js/mermaid](https://link.zhihu.com/?target=https%3A//github.com/mermaid-js/mermaid)（需要将梯子设置成全局模式才能访问）

## 破坏语法的特殊字符

❕ 将文本放在引号内一遍渲染复杂字符
> graph LR;
> id1["(TEXT)"]
> 此处不加引号会出错
```mermaid
graph LR;
id1["(TEXT)"]
```
## 饼状图

**表类型关键字**: `pie`
**表名**:  `title`
例子:
```mermaid
pie
    title 为什么总是宅在家里？
    "喜欢宅" : 15
    "天气太热或太冷" : 20
    "穷" : 500
```
## 流程图

**表类型关键字**: `graph`

**方向**：用于开头，声明流程图的方向。
-   `graph`或`graph TB`或`graph TD`：从上往下
-   `graph BT`：从下往上
-   `graph LR`：从左往右
-   `graph RL`：从右往左
例子:
```mermaid
graph LR
    A[Start] --> B{Is it?};
    B -- Yes --> C[OK];
    C --> D[Rethink];
    D --> B;
    B -- No ----> E[End];
```


### 结点形状

**由节点边框控制形状**

```mermaid
graph
    默认方形
    id1[方形]
    id2(圆边矩形)
    id3([体育场形])
    id4[[子程序形]]
```

```mermaid
graph
	id1{菱形}
	id2{{六角形}}
    id5[(圆柱形)]
    id6((圆形))
	id6[\反向梯形/]
```

```mermaid
graph
	id3[/平行四边形/]
	id4[\反向平行四边形\]
	id5[/梯形\]
```

### 连线形状

**由书写格式控制**

```mermaid
graph LR
a-->b--文本1-->c-->|文本2|d
```
```mermaid
graph LR
a==>b==文本==>c
```
```mermaid
graph LR
a-.->b-.文本.->c
```
```mermaid
graph LR
a---b
b--文本1!---c
c---|文本2|d
d===e
e==文本3===f
f-.-g
g-.文本.-h
```
```mermaid
graph LR
    A[Start] --> B{Is it?};
    B -->|Yes| C[OK];
    C --> D[Rethink];
    D --> B;
    B --->|No| E[End];
```
```mermaid
graph 
   a --> b & c--> d
   
   A & B--> C & D
   
    X --> M
    X --> N
    Y --> M
    Y --> N
```

## 子代码块流程图

**图形关键字**: `flowchart `

**块状开始定义**: `subgraph `

**块状结束定义**: `end`

例子:
```mermaid
flowchart TB
    c1-->a2
    subgraph one
    a1-->a2
    end
    subgraph two
    b1-->b2
    end
    subgraph three
    c1-->c2
    end
    one --> two
    three --> two
    two --> c2
```

## 注释

在行首加入`%%`即可。