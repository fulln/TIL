---
dg-publish: true
title: SpringShell
createTime: 2023-07-02 01:27  
---

## 简介

1. 什么是springshell
  
并非所有应用程序都需要精美的 Web 用户界面。 有时，通过交互式终端与应用程序交互是完成任务的最合适方式。 Spring Shell 允许您创建这样一个可运行的应用程序，用户在其中输入文本命令，这些命令将一直运行直到程序终止。 Spring Shell 项目提供了创建此类 REPL（读取、评估、打印循环）应用程序的基础架构，让您可以专注于使用熟悉的 Spring 编程模型来实现命令。 Spring Shell 包含高级功能（例如解析、制表符补全、输出着色、精美的 ASCII-art 表格显示、输入转换和验证），使您能够专注于核心命令逻辑。

https://docs.spring.io/spring-shell/docs/3.1.2/docs/index.html

## 开始

> [!WARNING] _Spring Shell_ is based on _Spring Boot_ 3.1.1 and _Spring Framework_ 6.0.10 and thus requires _JDK 17_.

### 引入jar包

```
<properties>
    <spring-shell.version>3.1.2</spring-shell.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-shell-starter</artifactId>
    </dependency>
</dependencies>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.shell</groupId>
            <artifactId>spring-shell-dependencies</artifactId>
            <version>${spring-shell.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

```

然后等待启动类加载

```log
> Task :compileJava
> Task :processResources UP-TO-DATE
> Task :classes

> Task :FShellApplication.main()

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v3.1.1)

2023-07-02T01:33:20.538+08:00  INFO 20336 --- [           main] com.fulln.FShellApplication              : Starting FShellApplication using Java 17.0.6 with PID 20336 (C:\opt\work\FShell\build\classes\java\main started by fulln in C:\opt\work\FShell)
2023-07-02T01:33:20.538+08:00  INFO 20336 --- [           main] com.fulln.FShellApplication              : No active profile set, falling back to 1 default profile: "default"
2023-07-02T01:33:21.000+08:00  WARN 20336 --- [           main] org.jline                                : Unable to create a system terminal, creating a dumb terminal (enable debug logging for more information)
2023-07-02T01:33:21.188+08:00  INFO 20336 --- [           main] com.fulln.FShellApplication              : Started FShellApplication in 0.917 seconds (process running for 1.145)
shell:>

```

### 开始编写第一个命令

1. 类上添加注解 `@ShellComponent`
2. public 方法添加`@shellMethod`
3. 参数添加添加注解`@ShellOption`

```java
@ShellComponent  
public class HomeCommand {  
  
	@ShellMethod(value = "home", key = "f")  
	public String home(@ShellOption(defaultValue = "fulln") String name) {  
		return "Welcome to fulln's shell:"+name;  
	}  
}
```


