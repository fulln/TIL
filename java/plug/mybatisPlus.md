## mybatis-plus 通过lambda 获取属性名

mybatis-plus通过lamda表达式获取对应的字段名称,很方便, 看下其中是如何实现

### 代码剖析

首先,从mysql-plus提供的任何sql方法都可以找到`column`源码,如下面的`eq`

```java
@Override
public Children eq(boolean condition, R column, Object val) {
        return addCondition(condition, column, EQ, val);
}
//调用的就是如下方法
protected Children addCondition(boolean condition, R column, SqlKeyword sqlKeyword, Object val) {
        return doIt(condition, () -> 			columnToString(column), sqlKeyword, () -> formatSql("{0}", val));
}
```

可以看到获取字段名称是调用的`columnToString`方法,我们从中点进去再分析

```java
	protected String columnToString(SFunction<T, ?> 	column, boolean onlyColumn) {
        return getColumn(LambdaUtils.resolve(column), onlyColumn);
	}

	/** 
	看到LambdaUtils如下调用,这里只是加了个缓存,而且这里map的value被设置成了弱引用,不定被gc回收掉
  	*/
	public static <T> SerializedLambda resolve(SFunction<T, ?> func) {
        Class<?> clazz = func.getClass();
        return Optional.ofNullable(FUNC_CACHE.get(clazz))
            .map(WeakReference::get)
            .orElseGet(() -> {
                SerializedLambda lambda = SerializedLambda.resolve(func);
                FUNC_CACHE.put(clazz, new WeakReference<>(lambda));
                return lambda;
            });
	}
    /**
     * 通过反序列化转换 lambda 表达式，该方法只能序列化 lambda 表达式，不能序列化接口实现或者正常非 lambda 写法的对象
     *
     * @param lambda lambda对象
     * @return 返回解析后的 SerializedLambda
     */
    public static SerializedLambda resolve(SFunction<?, ?> lambda) {
        if (!lambda.getClass().isSynthetic()) {
            throw ExceptionUtils.mpe("该方法仅能传入 lambda 表达式产生的合成类");
        }
        try (ObjectInputStream objIn = new ObjectInputStream(new ByteArrayInputStream(SerializationUtils.serialize(lambda))) {
            //通过反序列化获取对应的java.lang.invoke.SerializedLambda的相关属性
            @Override
            protected Class<?> resolveClass(ObjectStreamClass objectStreamClass) throws IOException, ClassNotFoundException {
                Class<?> clazz = super.resolveClass(objectStreamClass);
                return clazz == java.lang.invoke.SerializedLambda.class ? SerializedLambda.class : clazz;
            }
        }) {
            //强转成自己封装的SerializedLambda
            return (SerializedLambda) objIn.readObject();
        } catch (ClassNotFoundException | IOException e) {
            throw ExceptionUtils.mpe("This is impossible to happen", e);
        }
    }


    
    /**
     将对象转换成字节流
     * Serialize the given object to a byte array.
     * @param object the object to serialize
     * @return an array of bytes representing the object in a portable fashion
     */
    public static byte[] serialize(Object object) {
        if (object == null) {
            return null;
        }
        ByteArrayOutputStream baos = new ByteArrayOutputStream(1024);
        try {
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(object);
            oos.flush();
        } catch (IOException ex) {
            throw new IllegalArgumentException("Failed to serialize object of type: " + object.getClass(), ex);
        }
        return baos.toByteArray();
    }

    /**
     * 获取 SerializedLambda 对应的列信息，从 lambda 表达式中推测实体类
     * <p>
     * 如果获取不到列信息，那么本次条件组装将会失败
     *
     * @param lambda     lambda 表达式
     * @param onlyColumn 如果是，结果: "name", 如果否： "name" as "name"
     * @return 列
     * @throws com.baomidou.mybatisplus.core.exceptions.MybatisPlusException 获取不到列信息时抛出异常
     * @see SerializedLambda#getImplClass()
     * @see SerializedLambda#getImplMethodName()
     */
    private String getColumn(SerializedLambda lambda, boolean onlyColumn) throws MybatisPlusException {
        // 获取到了字段的名称
        String fieldName = PropertyNamer.methodToProperty(lambda.getImplMethodName());
        // 获取字段的类型
        Class aClass = lambda.getInstantiatedMethodType();
        if (!initColumnMap) {
            columnMap = LambdaUtils.getColumnMap(aClass);
        }
        Assert.notNull(columnMap, "can not find lambda cache for this entity [%s]", aClass.getName());
        // 看看从类class里面能不能获取到对应字段名称
        ColumnCache columnCache = columnMap.get(LambdaUtils.formatKey(fieldName));
        Assert.notNull(columnCache, "can not find lambda cache for this property [%s] of entity [%s]",
            fieldName, aClass.getName());
        return onlyColumn ? columnCache.getColumn() : columnCache.getColumnSelect();
    }

```

### 总结

通过以上的操作可以使用lambda表达式来写对应的字段名称, 对于一些场景还是方便可靠的, 如果没有用过mybatis-plus的包下的utils, 可以把这些功能全部搬运到你当前做工作的项目下.


