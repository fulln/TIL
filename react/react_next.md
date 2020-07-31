## 使用react+next+material 构建前端

### 初始化项目

- 新建目录
- npm 初始化

```
npm init -y
```
- next 项目初始化

```react
npm install --save react react-dom next
```

- 加载material-ui

```
npm install @material-ui/core
```

> 发现在materil-ui的 demo库里面有直接创建项目的方法,也可以直接用[它的项目的](https://github.com/mui-org/material-ui/tree/next/examples/nextjs)的方法进行初始化项目


### 运行项目

```
npm run dev
``` 

在控制台如果出现了`localhost:3000` 则说明启动成功，剩下的就是搬运对应组件并拼装出你想要的对应的页面了。

### 目标

- 将小站改成 库在github 并实现CICD的形式。


