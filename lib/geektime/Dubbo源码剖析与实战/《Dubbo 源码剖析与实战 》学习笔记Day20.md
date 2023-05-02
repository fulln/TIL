---
dg-publish: true
---

#java #dubbo #极客时间 

## 课程内容

### dubbo Compiler

源码地址`org.apache.dubbo.common.compiler.Compiler`

#### Javassist 编译

这里可以参考[[Javassist]]

```java

// org.apache.dubbo.common.bytecode.ClassGenerator#toClass(java.lang.Class<?>, java.lang.ClassLoader, java.security.ProtectionDomain)
public Class<?> toClass(Class<?> neighborClass, ClassLoader loader, ProtectionDomain pd) {
    if (mCtc != null) {
        mCtc.detach();
    }
    // 自增长类名尾巴序列号，类似 $Proxy_01.class 这种 JDK 代理名称的 01 数字
    long id = CLASS_NAME_COUNTER.getAndIncrement();
    try {
        // 从 ClassPool 中获取 mSuperClass 类的类型
        // 我们一般还可以用 mPool 来看看任意类路径对应的 CtClass 类型对象是什么
        // 比如可以通过 mPool.get("java.lang.String") 看看 String 的 CtClass 类型对象是什么
        // 之所以要这么做，主要是为了迎合这样的API语法而操作的
        CtClass ctcs = mSuperClass == null ? null : mPool.get(mSuperClass);
        if (mClassName == null) {
            mClassName = (mSuperClass == null || javassist.Modifier.isPublic(ctcs.getModifiers())
                    ? ClassGenerator.class.getName() : mSuperClass + "$sc") + id;
        }
        // 通过 ClassPool 来创建一个叫 mClassName 名字的类
        mCtc = mPool.makeClass(mClassName);
        if (mSuperClass != null) {
            // 然后设置一下 mCtc 这个新创建类的父类为 ctcs
            mCtc.setSuperclass(ctcs);
        }
        // 为 mCtc 新建类添加一个实现的接口
        mCtc.addInterface(mPool.get(DC.class.getName())); // add dynamic class tag.
        if (mInterfaces != null) {
            for (String cl : mInterfaces) {
                mCtc.addInterface(mPool.get(cl));
            }
        }
        // 为 mCtc 新建类添加一些字段
        if (mFields != null) {
            for (String code : mFields) {
                mCtc.addField(CtField.make(code, mCtc));
            }
        }
        // 为 mCtc 新建类添加一些方法
        if (mMethods != null) {
            for (String code : mMethods) {
                if (code.charAt(0) == ':') {
                    mCtc.addMethod(CtNewMethod.copy(getCtMethod(mCopyMethods.get(code.substring(1))),
                            code.substring(1, code.indexOf('(')), mCtc, null));
                } else {
                    mCtc.addMethod(CtNewMethod.make(code, mCtc));
                }
            }
        }
        // 为 mCtc 新建类添加一些构造方法
        if (mDefaultConstructor) {
            mCtc.addConstructor(CtNewConstructor.defaultConstructor(mCtc));
        }
        if (mConstructors != null) {
            for (String code : mConstructors) {
                if (code.charAt(0) == ':') {
                    mCtc.addConstructor(CtNewConstructor
                            .copy(getCtConstructor(mCopyConstructors.get(code.substring(1))), mCtc, null));
                } else {
                    String[] sn = mCtc.getSimpleName().split("\\$+"); // inner class name include $.
                    mCtc.addConstructor(
                            CtNewConstructor.make(code.replaceFirst(SIMPLE_NAME_TAG, sn[sn.length - 1]), mCtc));
                }
            }
        }
        // 将 mCtc 新创建的类转成 Class 对象
        try {
            return mPool.toClass(mCtc, neighborClass, loader, pd);
        } catch (Throwable t) {
            if (!(t instanceof CannotCompileException)) {
                return mPool.toClass(mCtc, loader, pd);
            }
            throw t;
        }
    } catch (RuntimeException e) {
        throw e;
    } catch (NotFoundException | CannotCompileException e) {
        throw new RuntimeException(e.getMessage(), e);
    }
}
```
改造代码需要注意 3 点。
1. 在获取各种类对应的 CtClass 类型对象时，可以通过从 ClassPool 的 get 方法中传入类路径得到。
2. 在对方法的入参字段名进行逻辑处理时，就得替换成 $ 占位符，方法中的 this 引用，用 $0 表示，方法中的第一个参数用 $1 表示，第二个参数用 $2 表示，以此类推。
3. 若要重写的父类的方法，是否设置 @Override 属性不太重要，但是千万别为了重写而拿父类的 CtMethod 属性一顿乱改。

#### ASM 编译

> 可以参考[[ASM 字节码技术]]

ASM 是一款侧重于性能的字节码插件，属于一种轻量级的高性能字节码插件，但同时实现的难度系数也会变大

- 设计一个代码模板。
- 其次，通过 IDEA 的协助得到代码模板的字节码指令内容
- 。然后，使用 Asm 的相关 API 依次将字节码指令翻译为 Asm 对应的语法，比如创建 ClassWriter 相当于创建了一个类，继续调用 ClassWriter.visitMethod 方法相当于创建了一个方法等等，对于生僻的字节码指令实在找不到对应的官方文档的话，可以通过“MethodVisitor + 字节码指令”来快速查找对应的 Asm API。
- 最后，调用 ClassWriter.toByteArray 得到字节码的字节数组，传递到 ClassLoader.defineClass 交给 JVM 虚拟机得出一个 Class 类信息。

#### 使用场景

- JavaCompiler：是 JDK 提供的一个工具包，我们熟知的 Javac 编译器其实就是 JavaCompiler 的实现，不过 JDK 的版本迭代速度快，变化大，我们升级 JDK 的时候，本来在低版本 JDK 能正常编译的功能，跑到高版本就失效了。
- Groovy：属于第三方插件，功能很多很强大，几乎是开发小白的首选框架，不需要考虑过多 API 和字节码指令，会构建源代码字符串，交给 Groovy 插件后就能拿到类信息，拿起来就可以直接使用，但同时也是比较重量级的插件。
- Javassist：封装了各种 API 来创建类，相对于稍微偏底层的风格，可以动态针对已有类的字节码，调用相关的 API 直接增删改查，非常灵活，只要熟练使用 API 就可以达到很高的境界。
- ASM：是一个通用的字节码操作的框架，属于非常底层的插件了，操作该插件的技术难度相当高，需要对字节码指令有一定的了解，但它体现出来的性能却是最高的，并且插件本身就是定位为一款轻量级的高性能字节码插件。有了众多动态编译方式的法宝，从简单到复杂，从重量级到轻量级




## 课程地址

[16｜Compiler编译：神乎其神的编译你是否有过胆怯？]([16｜Compiler编译：神乎其神的编译你是否有过胆怯？ (geekbang.org)](https://time.geekbang.org/column/article/620921))