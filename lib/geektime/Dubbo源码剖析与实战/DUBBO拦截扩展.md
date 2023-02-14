#java #dubbo #极客时间 

## 拦截扩展：如何利用Filter进行扩展？

### Filter 拦截中主要使用到的场景

**前置、后置处理的环节中的增强**

包含关系中，把前置后置逻辑与业务功能的代码写在一个地方，通过一些代码设计，做方法的封装，尽量隔离关联性，但难保后续的迭代。

分离关系和现有的业务功拉开距离，要么会偏技术属性，要么会偏业务属性。偏技术属性的功能，尽量少和业务功能发生关系。

####  数据加解密

1. 包含关系会导致原方法膨胀，后续维护难度上升
2. 分离关系需要分清属于业务属性还是技术属性。技术属性就可以从统一拦截入手，既满足通用又零侵入。


```java 

///////////////////////////////////////////////////                  
// 提供方：解密过滤器，仅在提供方有效，因为 @Activate 注解中设置的是 PROVIDER 侧
// 功能：通过 “类名 + 方法名” 从配置中心获取解密配置，有值就执行解密操作，没值就跳过
///////////////////////////////////////////////////
@Activate(group = PROVIDER)
public class DecryptProviderFilter implements Filter {

    /** <h2>配置中心 AES 密钥的配置名称，通过该名称就能从配置中心拿到对应的密钥值</h2> **/
    public static final String CONFIG_CENTER_KEY_AES_SECRET = "CONFIG_CENTER_KEY_AES_SECRET";

    @Override
    public Result invoke(Invoker<?> invoker, Invocation invocation) throws RpcException {
        // 从 OPS 配置中心里面获取到 aesSecretOpsKey 对应的密钥值
        String privateKey = OpsUtils.getAesSecret(CONFIG_CENTER_KEY_AES_SECRET);

        // 获取此次请求的类名、方法名，并且构建出一个唯一的 KEY
        String serviceName = invocation.getServiceModel().getServiceKey();
        String methodName = RpcUtils.getMethodName(invocation);
        String uniqueKey = String.join("_", serviceName, methodName);

        // 通过唯一 KEY 从配置中心查询出来的值为空，则说明该方法不需要解密
        // 那么就当作什么事也没发生，继续走后续调用逻辑
        String configVal = OpsUtils.get(uniqueKey);
        if (StringUtils.isBlank(configVal)) {
            return invoker.invoke(invocation);
        }

        // 能来到这里说明通过唯一 KEY 从配置中心找到了配置，那么就直接将找到的配置值反序列化为对象
        DecryptConfig decryptConfig = JSON.parseObject(configVal, DecryptConfig.class);
        // 循环解析配置中的所有字段列表，然后挨个解密并回填明文值
        for (String fieldPath : decryptConfig.getFieldPath()) {
            // 通过查找节点工具类，通过 fieldPath 字段路径从 invocation 中找出对应的字段值
            String encryptContent = PathNodeUtils.failSafeGetValue(invocation, fieldPath);
            // 找出来的字段值为空的话，则不做任何处理，继续处理下一个字段
            if (StringUtils.isBlank(encryptContent)) {
                continue;
            }

            // 解密成为明文后，则继续将明文替换掉之前的密文
            String plainContent = AesUtils.decrypt(encryptContent, privateKey);
            PathNodeUtils.failSafeSetValue(invocation, fieldPath, plainContent);
        }

        // 能来到这里，说明解密完成，invocation 中已经是明文数据了，然后继续走后续调用逻辑
        return invoker.invoke(invocation);
    }

    /**
     * <h1>解密配置。</h1>
     */
    @Setter
    @Getter
    public static class DecryptConfig {
        List<String> fieldPath;
    }
}

///////////////////////////////////////////////////
// 提供方资源目录文件
// 路径为：/META-INF/dubbo/org.apache.dubbo.rpc.Filter
///////////////////////////////////////////////////
decryptProviderFilter=com.hmilyylimh.cloud.filter.config.DecryptProviderFilter
```

#### 常见拦截扩展机制

1. SpringMvc 拦截器扩展，通过扩展 org.springframework.web.servlet.HandlerInterceptor 接口，就可以在控制器的方法执行之前、成功之后、异常时，进行扩展处理。
2. Mybatis 的拦截器，通过扩展 org.apache.ibatis.plugin.Interceptor 接口，可以拦截执行的 SQL 方法，在方法之前、之后进行扩展处理。
3. Spring 的 BeanDefinition 后置处理器，通过扩展 org.springframework.beans.factory.config.BeanFactoryPostProcessor 接口，可以针对扫描出来的 BeanDefinition 对象进行修改操作，改变对象的行为因素。
4. ...


## 地址

此文章为2月day9 学习笔记，内容来源于极客时间《[24｜拦截扩展：如何利用Filter进行扩展？ (geekbang.org)](https://time.geekbang.org/column/article/625375)》，推荐该课程