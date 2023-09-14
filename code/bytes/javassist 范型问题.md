---
dg-publish: true
createTime: 2023-01-27 12:49
tags:
  - java
  - javabasic
  - 字节码增强
  - javassist
---
## 问题现状

代码:
```java
		StringBuffer stringBuffer = new StringBuffer();
        stringBuffer.append("{\n");
        stringBuffer.append("Map<String, String> tags = new HashMap<>();");
        stringBuffer.append("\n}");
 
        newCtMethod.setBody(stringBuffer.toString());
        ctClass.addMethod(newCtMethod);
```

遇到的异常:
```java
javassist.CannotCompileException: [source error] ; is missing
	at javassist.CtBehavior.setBody(CtBehavior.java:474)
	at javassist.CtBehavior.setBody(CtBehavior.java:440)
	at com.example.demo.proxy.DemoClass.javassistGenerator(DemoClass.java:37)
	at com.example.demo.proxy.DemoClass.main(DemoClass.java:71)
Caused by: javassist.compiler.CompileError: ; is missing
	at javassist.compiler.Parser.parseDeclarationOrExpression(Parser.java:611)
	at javassist.compiler.Parser.parseStatement(Parser.java:295)
	at javassist.compiler.Parser.parseBlock(Parser.java:307)
	at javassist.compiler.Parser.parseStatement(Parser.java:261)
	at javassist.compiler.Javac.compileBody(Javac.java:219)
	at javassist.CtBehavior.setBody(CtBehavior.java:466)
	... 3 common frames omitted
```

## 代码追踪

通过上面堆栈,可以很明显发现异常来自于`parseDeclarationOrExpression`代码和注释如下
```java
/* declaration.or.expression  
 *      : [ FINAL ] built-in-type array.dimension declarators
 *      | [ FINAL ] class.type array.dimension declarators 
 *      | expression ';' 
 *      | expr.list ';'             if exprList is true 
 * * Note: FINAL is currently ignored.  This must be fixed
 * in future. 
 *
 */
private Stmnt parseDeclarationOrExpression(SymbolTable tbl,  
                                           boolean exprList)  
    throws CompileError  
{  
    int t = lex.lookAhead();  
    while (t == FINAL) {  
        lex.get();  
        t = lex.lookAhead();  
    }  
  
    if (isBuiltinType(t)) {  
        t = lex.get();  
        int dim = parseArrayDimension();  
        return parseDeclarators(tbl, new Declarator(t, dim));  
    }  
    else if (t == Identifier) {  
        int i = nextIsClassType(0);  
        if (i >= 0)  
            if (lex.lookAhead(i) == Identifier) {  
                ASTList name = parseClassType(tbl);  
                int dim = parseArrayDimension();  
                return parseDeclarators(tbl, new Declarator(name, dim));  
            }  
    }  
  
    Stmnt expr;  
    if (exprList)  
        expr = parseExprList(tbl);  
    else        expr = new Stmnt(EXPR, parseExpression(tbl));  
  
    if (lex.get() != ';')  
        throw new CompileError("; is missing", lex);  
  
    return expr;  
}
```

可见根据方法上注释, 无法识别`<>` 这种范型的代码,google后发现javassist中写入函数体中含有范型时
1. 对于范型符号需要特殊处理
2. 对引用的外部类显式声明包路径

### 修改

将demo代码修改如下

```java
		StringBuffer stringBuffer = new StringBuffer();
        stringBuffer.append("{\n");
        stringBuffer.append("Map tags = new HashMap();");
        stringBuffer.append("\n}");
        newCtMethod.setBody(stringBuffer.toString());
        ctClass.addMethod(newCtMethod);
```

### 参考文章

> https://blog.csdn.net/kakaweb/article/details/84592472