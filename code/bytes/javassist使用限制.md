#javassist  #字节码增强 

http://www.javassist.org/tutorial/tutorial2.html#limit

## 使用限制

在当前的实现中，Javassist 中包含的 Java 编译器在编译器可以接受的语言方面有一些限制。这些限制是：

-   不支持 J2SE 5.0 引入的新语法（包括枚举和泛型）。Javassist 的低级 API 支持注解。请参阅`javassist.bytecode.annotation`包（以及`getAnnotations()` 在`CtClass`和中`CtBehavior`）。也仅部分支持泛型。有关更多详细信息，请参阅[后面的部分](http://www.javassist.org/tutorial/tutorial3.html#generics)。
    
-   `{`数组初始值设定项是用大括号和括起来的以逗号分隔的表达式列表，`}`除非数组维度为一，否则不可用。
    
-   不支持内部类或匿名类。请注意，这只是编译器的限制。它无法编译包含匿名类声明的源代码。Javassist 可以读取和修改内部/匿名类的类文件。
    
-   不支持 标签`continue`和语句。`break`
    
-   编译器没有正确实现 Java 方法分派算法。如果类中定义的方法具有相同的名称但采用不同的参数列表，编译器可能会混淆。
    
    例如，
    
    A类{}
    B 类扩展 A {}
    C 类扩展 B {}
    类 X {
        void foo(A a) { .. }
        void foo(B b) { .. }
    }
    
    如果编译后的表达式是X 的实例`x.foo(new C())`，其中 `x`是 X 的实例，编译器可能会调用 ，`foo(A)`尽管编译器可以正确编译 `foo((B)new C())`。
    
-   建议用户使用`#`作为类名和静态方法或字段名之间的分隔符。例如，在常规 Java 中，
    
    javassist.CtClass.intType.getName()
    
    `getName()`在 中的静态字段指示的对象上`intType` 调用方法`javassist.CtClass`。在 Javassist 中，用户可以编写如上所示的表达式，但建议他们编写：
    
    javassist.CtClass#intType.getName()
    
    以便编译器可以快速解析表达式。