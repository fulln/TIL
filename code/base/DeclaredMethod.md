---
dg-publish: true
---
#java #反射

## java反射使用getDeclaredMethods

最近在使用`getDeclaredMethods`方法获取类中的方法时碰到奇怪的问题，先来看看`getDeclaredMethods`方法的注释：

```java
/**
 *
 * Returns an array containing {@code Method} objects reflecting all the
 * declared methods of the class or interface represented by this {@code
 * Class} object, including public, protected, default (package)
 * access, and private methods, but excluding inherited methods.
 *
 * <p> If this {@code Class} object represents a type that has multiple
 * declared methods with the same name and parameter types, but different
 * return types, then the returned array has a {@code Method} object for
 * each such method.
 *
 * <p> If this {@code Class} object represents a type that has a class
 * initialization method {@code <clinit>}, then the returned array does
 * <em>not</em> have a corresponding {@code Method} object.
 *
 * <p> If this {@code Class} object represents a class or interface with no
 * declared methods, then the returned array has length 0.
 *
 * <p> If this {@code Class} object represents an array type, a primitive
 * type, or void, then the returned array has length 0.
 *
 * <p> The elements in the returned array are not sorted and are not in any
 * particular order.
 *
 * @return  the array of {@code Method} objects representing all the
 *          declared methods of this class
 * @throws  SecurityException
 *          If a security manager, <i>s</i>, is present and any of the
 *          following conditions is met:
 *
 *          <ul>
 *
 *          <li> the caller's class loader is not the same as the
 *          class loader of this class and invocation of
 *          {@link SecurityManager#checkPermission
 *          s.checkPermission} method with
 *          {@code RuntimePermission("accessDeclaredMembers")}
 *          denies access to the declared methods within this class
 *
 *          <li> the caller's class loader is not the same as or an
 *          ancestor of the class loader for the current class and
 *          invocation of {@link SecurityManager#checkPackageAccess
 *          s.checkPackageAccess()} denies access to the package
 *          of this class
 *
 *          </ul>
 *
 * @jls 8.2 Class Members
 * @jls 8.4 Method Declarations
 * @since JDK1.1
 * 1.返回一个包含Method对象的数组，该对象反映了此Class对象表示的类或接口的所有声明方法，包括公共、受保护、默认（包）访问和私有方法，但不包括继承的方法。
 * 2.如果此Class对象表示一个类型，该类型具有多个具有相同名称和参数类型但返回类型不同的声明方法，则 返回的数组对于每个此类方法都有一个Method对象。
 * 3.如果此Class对象表示具有类初始化方法的类型<clinit>则 返回的阵列不具有相应的Method的对象。(不返回构造参数)
 * 4.如果此Class对象表示没有声明方法的类或接口，则返回的数组长度为 0。
 * 5.如果此Class对象表示数组类型、基本类型或 void，则返回的数组长度为 0。
 * 6.返回的数组中的元素没有排序，也没有任何特定的顺序。 
 * 返回：
 * 表示此类的所有声明方法的Method对象数组
 * 抛出：
 * SecurityException – 如果存在安全管理器s并且满足以下任何条件：
 * 调用者的类加载器与此类的类加载器不同，并且使用RuntimePermission("accessDeclaredMembers")调用s.checkPermission方法拒绝访问此类中的声明方法
 * 调用者的类加载器与当前类的类加载器不同，或者不是该类加载器的祖先，并且调用s.checkPackageAccess()拒绝访问此类的包
 * 自从：JDK1.1
 * 外部注释：@org.jetbrains.annotations.NotNull @org.jetbrains.annotations.Contract(pure = true)
 */
@CallerSensitive
public Method[] getDeclaredMethods() throws SecurityException {
    checkMemberAccess(Member.DECLARED, Reflection.getCallerClass(), true);
    return copyMethods(privateGetDeclaredMethods(false));
}
```

### 顺序问题

在JDK的API文档里明确标注了(第6点)：不能保证getDeclaredFields()/getDeclaredMethods()返回的Fields[] 和 Methods[] 的顺序。注意是不能保证返回顺序，而不是返回是乱序：它完全可能是乱序，也还可能是按照声明顺序排布。

这是因为，JVM有权在编译时，自行决定类成员的顺序，不一定要按照代码中的声明顺序来进行编译。因此返回的顺序其实是class文件中的成员正向顺序，只不过在编译时这个顺序不一定等于声明时的顺序。

### 额外方法问题

JDK文档标明的第一点说不包括继承方法,但是在实际使用中,还是会发现有包含父类方法的情况,下面用案例展示

- 正常例子

  ```java
  public class  {
  
      class A {
          void add(Object obj) {
          }
      }
  
      class B extends A{
          
          void add(Object obj) {
          }
      }
  
      public static void main(String[] args) {
          for (Method method : B.class.getDeclaredMethods()) {
              System.out.println(method.toString());
          }
      }
  
  }
  ```

  这里执行结果为 

  ```java
  void com.fcbox.member.service.rights.domain.C$B.add(java.lang.Object)
  ```

  正常的只获取了子类中的methon

- 非正常例子

  ```java
  public class  C{
  
      class A<T> {
           void add(T t) {
          }
      }
  
      class B extends A<String>{
          
          void add(String obj) {
          }
      }
  
      public static void main(String[] args) {
          for (Method method : B.class.getDeclaredMethods()) {
              System.out.println(method.toString());
          }
      }
  }
  ```

  这里执行结果为

  ```java
  void com.fcbox.member.service.rights.domain.C$B.add(java.lang.String)
  void com.fcbox.member.service.rights.domain.C$B.add(java.lang.Object)
  ```

  发现把父类的方法也给查出来了

- 解决办法

  手动判断`method.isBridge()`来判断是不是继承了父类的方法的method

### 总结

使用反射的方法的时候,需要注意下对应api上面的描述,不然写了bug都不自知

- 参考

  > https://www.dazhuanlan.com/wangpine/topics/1571580
  >
  > https://blog.csdn.net/Shenpibaipao/article/details/78510849
