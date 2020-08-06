## java为啥会有static main?

### 为啥main 方法要static修饰

稍稍总结了一下,有以下几点
* static 表示在加载的时候是已经就已经进行了内存空间的分配,在后续使用的过程中就不用去通过创建实例去开辟内存空间再进行后续的调用
* 在启动过程中,是没有已初始化的任何实例的,所以只能通过main方法去调用

### 如何从static main启动

在当初学习java的启动会让通过命令行启动

```shell
java -c hello
```

然后**java.exe**怎样从**main**函数開始运行，启动虚拟机，并运行字节码中的代码
> 此处参考`深入理解java虚拟机`,使用版本为`openjdk`不作其他表述

在一系列调用栈之后,最终会去调用`JavaMain(jdk8u/jdk/src/share/bin/java.c)`这个函数去加载各个类,并启动`main`函数

```c
int JNICALL
JavaMain(void * _args)
{
    JavaMainArgs *args = (JavaMainArgs *)_args;
    int argc = args->argc;
    char **argv = args->argv;
    int mode = args->mode;
    char *what = args->what;
    InvocationFunctions ifn = args->ifn;

    JavaVM *vm = 0;
    JNIEnv *env = 0;
    jclass mainClass = NULL;
    jclass appClass = NULL; // actual application class being launched
    jmethodID mainID;
    jobjectArray mainArgs;
    int ret = 0;
    jlong start, end;

    RegisterThread();

    /* Initialize the virtual machine */
    start = CounterGet();
    if (!InitializeJVM(&vm, &env, &ifn)) {
        JLI_ReportErrorMessage(JVM_ERROR1);
        exit(1);
    }

    ...

    ret = 1;

    /*
     * Get the application's main class.
     *
     * See bugid 5030265.  The Main-Class name has already been parsed
     * from the manifest, but not parsed properly for UTF-8 support.
     * Hence the code here ignores the value previously extracted and
     * uses the pre-existing code to reextract the value.  This is
     * possibly an end of release cycle expedient.  However, it has
     * also been discovered that passing some character sets through
     * the environment has "strange" behavior on some variants of
     * Windows.  Hence, maybe the manifest parsing code local to the
     * launcher should never be enhanced </font>.
     *
     * Hence, future work should either:
     *     1)   Correct the local parsing code and verify that the
     *          Main-Class attribute gets properly passed through
     *          all environments,
     *     2)   Remove the vestages of maintaining main_class through
     *          the environment (and remove these comments).
     *
     * This method also correctly handles launching existing JavaFX
     * applications that may or may not have a Main-Class manifest entry.
     */
    mainClass = LoadMainClass(env, mode, what);
    CHECK_EXCEPTION_NULL_LEAVE(mainClass);
    /*
     * In some cases when launching an application that needs a helper, e.g., a
     * JavaFX application with no main method, the mainClass will not be the
     * applications own main class but rather a helper class. To keep things
     * consistent in the UI we need to track and report the application main class.
     */
    appClass = GetApplicationClass(env);
    NULL_CHECK_RETURN_VALUE(appClass, -1);
    /*
     * PostJVMInit uses the class name as the application name for GUI purposes,
     * for example, on OSX this sets the application name in the menu bar for
     * both SWT and JavaFX. So we'll pass the actual application class here
     * instead of mainClass as that may be a launcher or helper class instead
     * of the application class.
     */
    PostJVMInit(env, appClass, vm);
    /*
     * The LoadMainClass not only loads the main class, it will also ensure
     * that the main method's signature is correct, therefore further checking
     * is not required. The main method is invoked here so that extraneous java
     * stacks are not in the application stack trace.
     */
    mainID = (*env)->GetStaticMethodID(env, mainClass, "main",
                                       "([Ljava/lang/String;)V");
    CHECK_EXCEPTION_NULL_LEAVE(mainID);

    /* Build platform specific argument array */
    mainArgs = CreateApplicationArgs(env, argv, argc);
    CHECK_EXCEPTION_NULL_LEAVE(mainArgs);

    /* Invoke main method. */
    (*env)->CallStaticVoidMethod(env, mainClass, mainID, mainArgs);

    /*
     * The launcher's exit code (in the absence of calls to
     * System.exit) will be non-zero if main threw an exception.
     */
    ret = (*env)->ExceptionOccurred(env) == NULL ? 0 : 1;
    LEAVE();
}
```
在上面的函数中，很明显的能看到从jvm启动，到mainclass加载，到main方法启动，自此之后就都是java的范畴了，

### 观察注释

在调用
```c
GetApplicationClass
```
这个方法的时候，可以观察它的注释
**在一些情况下如果没有自己申明main方法启动容器，会直接启动容器中的main**

```c
GetStaticMethodID
```
**在启动main方法的时候需要注册一个main方法的名字,以免追踪到的无关main方法的堆栈**

如果深入到这个方法中，我们可以看到下面的代码
```c
/*make sure it's static, not virtual+private */
if(meth != NULL && !dvmIsStaticMethod(meth)) {

  IF_LOGD() {
  char*desc = dexProtoCopyMethodDescriptor(&meth->prototype);
  LOGD("GetStaticMethodID:"
    "notreturning nonstatic method %s.%s %s\n",clazz->descriptor,meth->name, desc);
  free(desc);
  }
  meth = NULL;
}

```

这个代码中判断找到的方法是静态的，而不是虚方法。找不到对应的静态方法就会直接抛出异常`dvmThrowException("Ljava/lang/NoSuchMethodError;",name);`


回到我们刚刚的java.c中,在最后去调用方法

```c
CallStaticVoidMethod
```
去执行main方法，完成java程序的启动






