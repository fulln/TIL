#java #javabasic 

## java 看加载的class 的来源

 主要是为了方便排查相同路径,的同名class 但是运行时jar包加的哪个不知道,有多个jar包都包含了该class的情况

使用方法

```java
xxx.class.getProtectionDomain().getCodeSource().getLocation()
```
