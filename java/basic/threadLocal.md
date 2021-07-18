## ThreadLocal 解析

### 简介

此类提供线程局部变量。 这些变量不同于它们的普通对应变量，因为每个访问一个（通过其get或set方法）的线程都有自己的、独立初始化的变量副本

> This class provides thread-local variables. These variables differ from their normal counterparts in that each thread that accesses one (via its get or set method) has its own, independently initialized copy of the variable. 

### 类关系

#### 构造方法

```java
/**
 无参构造方法
 */
public ThreadLocal() {
}

```



#### 成员变量

```java
/**
 在ThreadLocalMaps中, 用该值来校验 key的hash值 
 */
private final int threadLocalHashCode
/**
  要给出的下一个hashCode ,原子递增,从0开始
 */
private static AtomicInteger nextHashCode =
        new AtomicInteger();
/**
 连续生产的hashcode差异,将顺序生产的线程id转成最优分布的乘法hash值,用于2次方的表
 */
private static final int HASH_INCREMENT = 0x61c88647;

```



#### 实现方法

```java
/**
  当前线程私有默认值
  初始化线程值使用,默认为空,
  如果希望线程局部变量具有除null以外的初始值，则必须对ThreadLocal进行子类继承化，并覆盖此方法。
 */
protected T initialValue() {
        return null;
}
/**
 静态方法创建ThreadLocal,并指定初始化值,即赋值重写了`initialValue`方法
 */
public static <S> ThreadLocal<S> withInitial(Supplier<? extends S> supplier) {
        return new SuppliedThreadLocal<>(supplier);
}

/**
 返回当前线程的设置的值,如果为空,返回当前线程默认值
 */
public T get() {
        Thread t = Thread.currentThread();
    	// 从ThreadLocalMap中获取当前线程的存的线程私有值
        ThreadLocalMap map = getMap(t);
        if (map != null) {
            ThreadLocalMap.Entry e = map.getEntry(this);
            if (e != null) {
                @SuppressWarnings("unchecked")
                T result = (T)e.value;
                return result;
            }
        }
        return setInitialValue();
}
/**
 判断当前线程私有值是否存在
 */
boolean isPresent() {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        return map != null && map.getEntry(this) != null;
}
/**
初始化当前threadlocal的值
 */
private T setInitialValue() {
        // 获取当前默认值
        T value = initialValue();
        Thread t = Thread.currentThread();
    	// 获取当前线程的ThreadLocalMap
        ThreadLocalMap map = getMap(t);
        if (map != null) {
            // 如果有初始化过, 就将默认值放到Map
            map.set(this, value);
        } else {
            // 如果没有初始化过,就创建一个ThreadLocalmap
            createMap(t, value);
        }
    	// 如果当前线程私有类是终止类型的,就把当前线程私有class加到 当前线程维护的 终止时需要通知的线程私有Collection中
        if (this instanceof TerminatingThreadLocal) {
            TerminatingThreadLocal.register((TerminatingThreadLocal<?>) this);
        }
        return value;
}

/**
 当前线程的值设置为 value
 */
public void set(T value) {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null) {
            map.set(this, value);
        } else {
            createMap(t, value);
        }
}

/**
 删除此线程局部变量的当前线程值。
 如果该线程私有值是通过get初始化出来的默认值,
 它将会被`initialValue`方法重新初始化.可能会导致在当前线程多次调用`initialValue`方法
 */
public void remove() {
         ThreadLocalMap m = getMap(Thread.currentThread());
         if (m != null) {
             m.remove(this);
         }
}


/**
这个方法 会被 InheritableThreadLocal 子类覆盖
 获取当前线程私有的map,
 */
ThreadLocalMap getMap(Thread t) {
        return t.threadLocals;
}
/** 
 创建ThreadLocalMap子类
 这个方法 会被 InheritableThreadLocal 子类覆盖
 */
void createMap(Thread t, T firstValue) {
        t.threadLocals = new ThreadLocalMap(this, firstValue);
}
/**
 创建继承线程局部变量映射的工厂方法。 设计为仅从 Thread 构造函数调用
 */
static ThreadLocalMap createInheritedMap(ThreadLocalMap parentMap) {
    return new ThreadLocalMap(parentMap);
}
/*
 给子类`InheritableThreadLocal`提供,在这里写是为了方便提供`createInheritedMap`方法
 */
T childValue(T parentValue) {
    throw new UnsupportedOperationException();
}
```



#### 内部类ThreadLocalMap

该类是一种定制的哈希映射，仅适用于维护线程本地值,类是包私有的，以允许在`Thread` 中声明字段。 为了处理非常大和长期存在的值，map的entity使用 WeakReferences 作为键。 但是，由于不使用reference queue，因此只有在表开始耗尽空间时才能保证删除旧有值

```java

```

##### ThreadLocalMap的构造方法

```java
/**
 默认是有参的构造方法,要初始化的时候,必然带着具体的值过来初始化
 */ 
ThreadLocalMap(ThreadLocal<?> firstKey, Object firstValue) {
    table = new Entry[INITIAL_CAPACITY];
    // 当前线程的hashCode & 容量 -1  ==  当前hashCode mod 容量
    int i = firstKey.threadLocalHashCode & (INITIAL_CAPACITY - 1);
    table[i] = new Entry(firstKey, firstValue);
    size = 1;
    setThreshold(INITIAL_CAPACITY);
}
/**
 从父类的threadMap 初始化子类的map,只在createInheritedMap中倍调用,
 */
private ThreadLocalMap(ThreadLocalMap parentMap) {
            Entry[] parentTable = parentMap.table;
            int len = parentTable.length;
            setThreshold(len);
            table = new Entry[len];
			// 将父类的所有的值一个个加到子类的map中
            for (Entry e : parentTable) {
                if (e != null) {
                    @SuppressWarnings("unchecked")
                    ThreadLocal<Object> key = (ThreadLocal<Object>) e.get();
                    if (key != null) {
                        // 设置子类的值
                        Object value = key.childValue(e.value);
                        Entry c = new Entry(key, value);
                        int h = key.threadLocalHashCode & (len - 1);
                        // 如果当前已经有值存在, 就获取下一个index
                        while (table[h] != null)
                            h = nextIndex(h, len);
                        table[h] = c;
                        size++;
                    }
                }
            }
        }
```

##### ThreadLocalMap的内部类

```java
/**
 弱引用class ,由于不使用reference queue，因此只有在表开始耗尽空间时才能保证删除旧有值 和软引用一样
 */
static class Entry extends WeakReference<ThreadLocal<?>> {
    /** The value associated with this ThreadLocal. */
    Object value;

    Entry(ThreadLocal<?> k, Object v) {
        super(k);
        value = v;
    }
}
```

##### 成员变量

```java
/**
初始化容量大小, 默认16  也必须是2的指数倍
 * The initial capacity -- MUST be a power of two.
 */
private static final int INITIAL_CAPACITY = 16;

/**
 map桶,根据需要进行扩容
 * The table, resized as necessary.
 * table.length MUST always be a power of two.
 */
private Entry[] table;

/**
 * The number of entries in the table.
 */
private int size = 0;

/**
  下次扩容的负载值, 和map类似
 * The next size value at which to resize.
 */
private int threshold; // Default to 0
```

##### 方法列表

```java
/**
 * Set the resize threshold to maintain at worst a 2/3 load factor.
 设置负载因子大小
 */
private void setThreshold(int len) {
    threshold = len * 2 / 3;
}

/**
 * Increment i modulo len.
 下一个可以插入的index,不然从0开始找
 */
private static int nextIndex(int i, int len) {
    return ((i + 1 < len) ? i + 1 : 0);
}
/**
上一个可以插入的index,不然从length-1 开始
 */
private static int prevIndex(int i, int len) {
            return ((i - 1 >= 0) ? i - 1 : len - 1);
}

/**
  根据threadLocal 获取 entity
  这方法只根据key &(length -1) 去获取对应value,  如果获取不到调用`getEntryAfterMiss`方法
 */
private Entry getEntry(ThreadLocal<?> key) {
            int i = key.threadLocalHashCode & (table.length - 1);
            Entry e = table[i];
    		//
            if (e != null && e.get() == key)
                return e;
            else
                return getEntryAfterMiss(key, i, e);
}
/**
  当在hash散列中找不到密钥时使用的 getEntry 方法的版
 */
private Entry getEntryAfterMiss(ThreadLocal<?> key, int i, Entry e) {
            Entry[] tab = table;
            int len = tab.length;

            while (e != null) {
                ThreadLocal<?> k = e.get();
                if (k == key)
                    return e;
                if (k == null)
                    //删除不用的实体
                    // 伴随着rehash
                    expungeStaleEntry(i);
                else
                    //使用nextInt 来找
                    i = nextIndex(i, len);
                e = tab[i];
            }
            return null;
}
// 设置值
private void set(ThreadLocal<?> key, Object value) {

            // We don't use a fast path as with get() because it is at
            // least as common to use set() to create new entries as
            // it is to replace existing ones, in which case, a fast
            // path would fail more often than not.
			//  不用快速寻址的方式, 在这个map中, 直接setvalue 和 通过换位置设置value 同样多 
    		//  在这种情况下，快速路径通常会失败.
            Entry[] tab = table;
            int len = tab.length;
            int i = key.threadLocalHashCode & (len-1);

            for (Entry e = tab[i];
                 e != null;
                 e = tab[i = nextIndex(i, len)]) {
                
                ThreadLocal<?> k = e.get();
				// 初始化的时候就会默认占坑位
                if (k == key) {
                    // 在这里替换默认值就行
                    e.value = value;
                    return;
                }
				// 如果有值,但是key是空,
                // 将之前的value替换为指定key-val ,无论是否已经存在
                if (k == null) {
                    replaceStaleEntry(key, value, i);
                    return;
                }
            }
			
	   		// 经过循环中的判断筛选最终还未找到目标值，则新建Entry存储，此时的i就是最终筛选出的正确位置。
            tab[i] = new Entry(key, value);
            int sz = ++size;
    		// 判断下是否要rehash
            if (!cleanSomeSlots(i, sz) && sz >= threshold)
                rehash();
}
/**
 删除不用的实体
 */
 private int expungeStaleEntry(int staleSlot) {
            Entry[] tab = table;
            int len = tab.length;
			// 这个index上的值要删除掉
            // expunge entry at staleSlot
            tab[staleSlot].value = null;
            tab[staleSlot] = null;
            size--;
			//缩容之后需要rehash
            // Rehash until we encounter null
            Entry e;
            int i;
     		// 一个个重新计算对应的坑位是多少
            for (i = nextIndex(staleSlot, len);
                 (e = tab[i]) != null;
                 i = nextIndex(i, len)) {
                ThreadLocal<?> k = e.get();
                //如果ThreadLocal是空的,就删除掉这个空的并返回,
                if (k == null) {
                    e.value = null;
                    tab[i] = null;
                    size--;
                } else {
                    //重新计算下坑位的hash值
                    int h = k.threadLocalHashCode & (len - 1);
                    //如果发现和之前的值不一样了,
                    if (h != i) {
                        // 将之前的坑位设置为空
                        tab[i] = null;

                        // Unlike Knuth 6.4 Algorithm R, we must scan until
                        // null because multiple entries could have been stale.
                        // 扫这个hash的现有的值,如果有值的话,就放到这个指定坑位
                        // 没有的话就index+1
                        while (tab[h] != null)
                            h = nextIndex(h, len);
                        tab[h] = e;
                    }
                }
            }
            return i;
        }
	/**
	 重新包装或重新调整表格的大小。 首先扫描整个表，删除陈旧的条目。 如果这不能充分缩小表格的大小，将表格大小加倍
         * Re-pack and/or re-size the table. First scan the entire
         * table removing stale entries. If this doesn't sufficiently
         * shrink the size of the table, double the table size.
         */
   private void rehash() {
            expungeStaleEntries();

            // Use lower threshold for doubling to avoid hysteresis
            if (size >= threshold - threshold / 4)
                //重新扩容
                resize();
        }

		/** 扩容
         * Double the capacity of the table.
         */
        private void resize() {
            Entry[] oldTab = table;
            int oldLen = oldTab.length;
            int newLen = oldLen * 2;
            Entry[] newTab = new Entry[newLen];
            int count = 0;

            for (Entry e : oldTab) {
                if (e != null) {
                    //下面的操作和之前的清除旧entity一样
                    ThreadLocal<?> k = e.get();
                    if (k == null) {
                        e.value = null; // Help the GC
                    } else {
      					// 计算坑位index
                        int h = k.threadLocalHashCode & (newLen - 1);
                        //看坑位有没有值,有就index+1
                        while (newTab[h] != null)
                            h = nextIndex(h, newLen);
                        newTab[h] = e;
                        // 容量++
                        count++;
                    }
                }
            }
			// 设置负载因子
            setThreshold(newLen);
            size = count;
            table = newTab;
        }
```



#### HASH_INCREMENT 为啥是1640531527

hash_increment为十六进制`0x61c88647` 也就是十进制的1640531527,

* 当容量为2的指数值时,所有填充的值hash值最均匀

1640531527 正好为 2^32  * ((√5-1)/2) 也就是 乘以黄金比例，在这种情况下，与2的指数次幂 进行hash算法分布极为均匀

> 详细推导见 https://blog.csdn.net/lingchen881218/article/details/72823556



#### 为啥存在内存泄露问题

ThreadLocalMap使用ThreadLocal作为key，如果一个ThreadLocal没有外部强引用来引用它，那么系统 GC 的时候，这个ThreadLocal势必会被回收，这样一来，ThreadLocalMap中就会出现key为null的Entry，就没有办法访问这些key为null的Entry的value，如果当前线程再迟迟不结束的话，这些key为null的Entry的value就会一直存在一条强引用链：Thread Ref -> Thread -> ThreaLocalMap -> Entry -> value，而如果要回收掉，需要在set值的时候，在可能刚好调用对应坑位，执行 `replaceStaleEntry`时才能回收掉，这样就会造成内存泄漏。
