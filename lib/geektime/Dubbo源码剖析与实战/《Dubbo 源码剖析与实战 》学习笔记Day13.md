#java #dubbo #极客时间 

## 课程内容

### dubbo 参数验证

#### 主要参数验证方式

1. 简单验证,在使用到的地方去提供校验代码
2. 事件通知验证
	1. dubbo通知无论在通知机制的实现类中发生什么样的异常，最终都不会影响程序继续往后执行.
	2. 方便各处使用
3. 统一验证
		拦截所有请求，请求会触发过滤器的 invoke 方法,在需要校验的对象加上对应注解

 ##### dubbo 统一拦截
 
- 首先找到具有拦截机制的类，这里就是 org.apache.dubbo.rpc.Filter 过滤器。
- 找到该 org.apache.dubbo.rpc.Filter 过滤器的所有实现类。
- 认真阅读每个过滤器的类名，翻阅一下每个过滤器的类注释，看看有什么用。

可以看到,在`ValidationFilter (org.apache.dubbo.validation.filter)` 是已经有对应的参数校验.

##### dubbo参数校验的使用

`<dubbo:method name="save" validation="jvalidation" />`

在方法层面添加 validation 属性，并设置属性值为 jvalidation，这样就可以正常使用底层提供的参数校验机制了。

消费者:

```java

///////////////////////////////////////////////////
// 统一验证：消费方的一段调用下游 validateUser 的代码
///////////////////////////////////////////////////
@Component
public class InvokeDemoFacade {

    // 注意，@DubboReference 这里添加了 validation 属性
    @DubboReference(validation ＝ "jvalidation")
    private ValidationFacade validationFacade;
    
    // 一个简单的触发调用下游 ValidationFacade.validateUser 的方法
    public String invokeValidate(String id, String name, String sex) {
        return validationFacade.validateUser(new ValidateUserInfo(id, name, sex));
    }
}
```

生产者:
```java

///////////////////////////////////////////////////
// 统一验证：提供方的一段接收 validateUser 请求的代码
///////////////////////////////////////////////////
// 注意，@DubboService 这里添加了 validation 属性
@DubboService(validation ＝ "jvalidation")
@Component
public class ValidationFacadeImpl implements ValidationFacade {
    @Override
    public String validateUser(ValidateUserInfo userInfo) {
        // 这里就象征性的模拟下业务逻辑
        String retMsg = "Ret: "
                + userInfo.getId()
                + "," + userInfo.getName()
                + "," + userInfo.getSex();
        System.out.println(retMsg);
        return retMsg;
    }
}
```

#### 代码改造

1. 为调用下游的接口添加 validation 属性。
2. 从源码中寻找能提供校验规则的标准产物，也就是注解。
3. 在下游的方法入参对象中，为需要校验的字段添加注解。

dubbo validate代码
```java

// org.apache.dubbo.validation.filter.ValidationFilter.invoke
public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
    // Validation 接口的代理类被注入成功，且该调用的方法有 validation 属性
    if (validation != null && !invocation.getMethodName().startsWith("$")
            && ConfigUtils.isNotEmpty(invoker.getUrl().getMethodParameter(invocation.getMethodName(), "validation"))) {
        try {
            // 接着通过 url 中 validation 属性值，并且为该方法创建对应的校验实现类
            Validator validator = validation.getValidator(invoker.getUrl());
            if (validator != null) {
                // 若找到校验实现类的话，则真正开启对方法的参数进行校验
                validator.validate(invocation.getMethodName(), invocation.getParameterTypes(), invocation.getArguments());
            }
        } catch (RpcException e) {
            // RpcException 异常直接抛出去
            throw e;
        } catch (Throwable t) {
            // 非 RpcException 异常的话，则直接封装结果返回
            return AsyncRpcResult.newDefaultAsyncResult(t, invocation);
        }
    }
    // 能来到这里，说明要么没有配置校验过滤器，要么就是校验了但参数都合法
    // 既然没有抛异常的话，那么就直接调用下一个过滤器的逻辑
    return invoker.invoke(invocation);
}

// org.apache.dubbo.validation.support.AbstractValidation.getValidator
public Validator getValidator(URL url) {
    // 将 url 转成字符串形式
    String key = url.toFullString();
    // validators 是一个 Map 结构，即底层可以说明每个方法都可以有不同的校验器
    Validator validator = validators.get(key);
    if (validator == null) {
        // 若通过 url 从 Map 结构中找不到 value 的话，则直接根据 url 创建一个校验器实现类
        // 而且 createValidator 是一个 protected abstract 修饰的
        // 说明是一种模板方式，创建校验器实现类，是可被重写重新创建自定义的校验器
        validators.put(key, createValidator(url));
        validator = validators.get(key);
    }
    return validator;
}

// org.apache.dubbo.validation.support.jvalidation.JValidation
public class JValidation extends AbstractValidation {
    @Override
    protected Validator createValidator(URL url) {
        // 创建一个 Dubbo 框架默认的校验器
        return new JValidator(url);
    }
}

// org.apache.dubbo.validation.support.jvalidation.JValidator
public class JValidator implements Validator {
    // 省略其他部分代码
    // 进入到 Dubbo 框架默认的校验器中，发现真实采用的是 javax 第三方的 validation 插件
    // 由此，我们应该找到了标准产物的关键突破口了
    private final javax.validation.Validator validator;
}
```

可以发现, 在最后采用的是 javax 第三方的 validation 插件

##### 自定义参数校验改造

```java
<dubbo:method name="save" validation="special" />

where "special" is representing a validator for special character.
special=xxx.yyy.zzz.SpecialValidation under META-INF folders org.apache.dubbo.validation.Validation file.
```

在 validation 属性的值上，填充一个自定义的校验类名，并且将自定义的校验类名添加到 META-INF 文件夹下的 org.apache.dubbo.validation.Validation 文件中。

#### 场景应用

第一，单值简单规则判断，各个字段的校验逻辑毫无关联、相互独立。
第二，提前拦截掉脏请求，尽可能把一些参数值不合法的情况提前过滤掉，对于消费方来说尽量把高质量的请求发往提供方，对于提供方来说，尽量把非法的字段值提前拦截，以此保证核心逻辑不被脏请求污染。
第三，通用网关校验领域，在网关领域部分很少有业务逻辑，但又得承接请求，对于不合法的参数请求就需要尽量拦截掉，避免不必要的请求打到下游系统，造成资源浪费。

## 课程地址

[07｜参数验证：写个参数校验居然也会被训？](https://time.geekbang.org/column/article/613339)