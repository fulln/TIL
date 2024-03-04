#java #spring #cache

## SpringCache 源码解析

#### @EnableCaching

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Import(CachingConfigurationSelector.class)
public @interface EnableCaching {
  /**是否要用cglib代理
   */
  boolean proxyTargetClass() default false;
  /**
  是否用proxy,还是用AspectJ
   */
  AdviceMode mode() default AdviceMode.PROXY;
  /**
   bean 创建顺序
   */
  int order() default Ordered.LOWEST_PRECEDENCE;
}
```

注解中的几个参数还是比较熟悉,经常在spring其他注解中看到,在class上看到使用import注解创建了一个bean`CachingConfigurationSelector`,点入可以发现3种cache不同的实现,对应上面列出的代理模式,我们选择默认的代理模式所选择的class继续往下走

> ```java
> org.springframework.cache.jcache.config.ProxyCachingConfiguration
> ```

```java
@Configuration
@Role(BeanDefinition.ROLE_INFRASTRUCTURE)
public class ProxyCachingConfiguration extends AbstractCachingConfiguration {

	@Bean(name = CacheManagementConfigUtils.CACHE_ADVISOR_BEAN_NAME)
	@Role(BeanDefinition.ROLE_INFRASTRUCTURE)
	public BeanFactoryCacheOperationSourceAdvisor cacheAdvisor() {
		BeanFactoryCacheOperationSourceAdvisor advisor = new BeanFactoryCacheOperationSourceAdvisor();
		advisor.setCacheOperationSource(cacheOperationSource());
		advisor.setAdvice(cacheInterceptor());
		if (this.enableCaching != null) {
			advisor.setOrder(this.enableCaching.<Integer>getNumber("order"));
		}
		return advisor;
	}

	@Bean
	@Role(BeanDefinition.ROLE_INFRASTRUCTURE)
	public CacheOperationSource cacheOperationSource() {
		return new AnnotationCacheOperationSource();
	}

	@Bean
	@Role(BeanDefinition.ROLE_INFRASTRUCTURE)
	public CacheInterceptor cacheInterceptor() {
		CacheInterceptor interceptor = new CacheInterceptor();
		interceptor.configure(this.errorHandler, this.keyGenerator, this.cacheResolver, this.cacheManager);
		interceptor.setCacheOperationSource(cacheOperationSource());
		return interceptor;
	}

}
```

又变成了熟悉的aop3架马车: pointCut 目标切面  -> inteceptor 处理逻辑 -> advisor 访问器,

- advisor

  生成代理类后, 执行对应方法时实际上实行的对象

  > org.springframework.cache.interceptor.BeanFactoryCacheOperationSourceAdvisor

- pointcut
  一直最寻下去,发现其能被增强的bean判断在`org.springframework.cache.jcache.interceptor.JCacheOperationSourcePointcut`

  ```java
  	@Override
  	public boolean matches(Method method, Class<?> targetClass) {
  		CacheOperationSource cas = getCacheOperationSource();
  		return (cas != null && !CollectionUtils.isEmpty(cas.getCacheOperations(method, targetClass)));
  	}
  ```

  往后面走即是在`AnnotationCacheOperationSource`调用的`getCacheOperations`方法,即调用的父类方法

  ```java
  if (method.getDeclaringClass() == Object.class) {
  			return null;
  		}
  
  		Object cacheKey = getCacheKey(method, targetClass);
  		Collection<CacheOperation> cached = this.attributeCache.get(cacheKey);
  
  		if (cached != null) {
  			return (cached != NULL_CACHING_ATTRIBUTE ? cached : null);
  		}
  		else {
              // 具体判断逻辑由此入
  			Collection<CacheOperation> cacheOps = computeCacheOperations(method, targetClass);
  			if (cacheOps != null) {
  				if (logger.isTraceEnabled()) {
  					logger.trace("Adding cacheable method '" + method.getName() + "' with attribute: " + cacheOps);
  				}
  				this.attributeCache.put(cacheKey, cacheOps);
  			}
  			else {
  				this.attributeCache.put(cacheKey, NULL_CACHING_ATTRIBUTE);
  			}
  			return cacheOps;
  		}
  ```

  再深入多层,发现我们常用的注解

  > org.springframework.cache.annotation.SpringCacheAnnotationParser#parseCacheAnnotations(org.springframework.cache.annotation.SpringCacheAnnotationParser.DefaultCacheConfig, java.lang.reflect.AnnotatedElement, boolean)

  ```java
  @Nullable
  	private Collection<CacheOperation> parseCacheAnnotations(
  			DefaultCacheConfig cachingConfig, AnnotatedElement ae, boolean localOnly) {
          // 2 者的区别在于 注解查询策略不  
          //getall -> INHERITED_ANNOTATIONS, 查找所有直接声明的注释以及任何@Inherited超类注释。 此策略仅在与Class类型一起使用时才真正有用，因为所有其他带注释的元素都忽略了@Inherited注释。 此策略不搜索已实现的接口
          //findall -> TYPE_HIERARCHY 对整个类型层次结构进行全面搜索，包括超类和实现的接口。 超类注释不需要使用@Inherited进行元注释。
  		Collection<? extends Annotation> anns = (localOnly ?
  				AnnotatedElementUtils.getAllMergedAnnotations(ae, CACHE_OPERATION_ANNOTATIONS) :
  				AnnotatedElementUtils.findAllMergedAnnotations(ae, CACHE_OPERATION_ANNOTATIONS));
  		if (anns.isEmpty()) {
  			return null;
  		}
  
  		final Collection<CacheOperation> ops = new ArrayList<>(1);
  		anns.stream().filter(ann -> ann instanceof Cacheable).forEach(
  				ann -> ops.add(parseCacheableAnnotation(ae, cachingConfig, (Cacheable) ann)));
  		anns.stream().filter(ann -> ann instanceof CacheEvict).forEach(
  				ann -> ops.add(parseEvictAnnotation(ae, cachingConfig, (CacheEvict) ann)));
  		anns.stream().filter(ann -> ann instanceof CachePut).forEach(
  				ann -> ops.add(parsePutAnnotation(ae, cachingConfig, (CachePut) ann)));
  		anns.stream().filter(ann -> ann instanceof Caching).forEach(
  				ann -> parseCachingAnnotation(ae, cachingConfig, (Caching) ann, ops));
  		return ops;
  	}
  ```

  正是在这里指明去找到method或者是class上面是否有对应的4种注解,来确定该bean是否需要被增强处理,然后在后续`findCacheOperations`将对应注解转成CacheOperation

  ```java
  protected Collection<CacheOperation> parseCacheAnnotations(DefaultCacheConfig cachingConfig, AnnotatedElement ae) {
  		Collection<CacheOperation> ops = null;
  
  		Collection<Cacheable> cacheables = AnnotatedElementUtils.getAllMergedAnnotations(ae, Cacheable.class);
  		if (!cacheables.isEmpty()) {
  			ops = lazyInit(ops);
  			for (Cacheable cacheable : cacheables) {
  				ops.add(parseCacheableAnnotation(ae, cachingConfig, cacheable));
  			}
  		}
  		Collection<CacheEvict> evicts = AnnotatedElementUtils.getAllMergedAnnotations(ae, CacheEvict.class);
  		if (!evicts.isEmpty()) {
  			ops = lazyInit(ops);
  			for (CacheEvict evict : evicts) {
  				ops.add(parseEvictAnnotation(ae, cachingConfig, evict));
  			}
  		}
  		Collection<CachePut> puts = AnnotatedElementUtils.getAllMergedAnnotations(ae, CachePut.class);
  		if (!puts.isEmpty()) {
  			ops = lazyInit(ops);
  			for (CachePut put : puts) {
  				ops.add(parsePutAnnotation(ae, cachingConfig, put));
  			}
  		}
  		Collection<Caching> cachings = AnnotatedElementUtils.getAllMergedAnnotations(ae, Caching.class);
  		if (!cachings.isEmpty()) {
  			ops = lazyInit(ops);
  			for (Caching caching : cachings) {
  				Collection<CacheOperation> cachingOps = parseCachingAnnotation(ae, cachingConfig, caching);
  				if (cachingOps != null) {
  					ops.addAll(cachingOps);
  				}
  			}
  		}
  
  		return ops;
  	}
  ```

  

- inteceptor

  > org.springframework.cache.interceptor.CacheInterceptor

  看下具体怎么处理缓存的,首先看代理类必然执行的`invoke`方法

  ```java
  @Override
  	public Object invoke(final MethodInvocation invocation) throws Throwable {
  		Method method = invocation.getMethod();
  
  		CacheOperationInvoker aopAllianceInvoker = new CacheOperationInvoker() {
  			@Override
  			public Object invoke() {
  				try {
  					return invocation.proceed();
  				}
  				catch (Throwable ex) {
  					throw new ThrowableWrapper(ex);
  				}
  			}
  		};
  
  		try {
  			return execute(aopAllianceInvoker, invocation.getThis(), method, invocation.getArguments());
  		}
  		catch (CacheOperationInvoker.ThrowableWrapper th) {
  			throw th.getOriginal();
  		}
  	}
  ```

  沿着execute一直往下走

  - 首先维护了cacheOperations上下文

  ```java
  public CacheOperationContexts(Collection<? extends CacheOperation> operations, Method method,
  				Object[] args, Object target, Class<?> targetClass) {
  			// 根据不同注解生成各自cacheOperation上下文
  			for (CacheOperation operation : operations) {
  				this.contexts.add(operation.getClass(), getOperationContext(operation, method, args, target, targetClass));
  			}
      		//  判断是否是线程同步
  			this.sync = determineSyncFlag(method);
  		}
  ```

  - 进行各个详细注解的处理

  ```java
  private Object execute(final CacheOperationInvoker invoker, Method method, CacheOperationContexts contexts) {
  		// 判断下这个method上面的是否有@Cacheable(sync=true) 限制缓存同步设置
          // unless()不支持
          // 只能指定一个缓存
          // 不能合并其他缓存相关的操作
  		if (contexts.isSynchronized()) {
  			CacheOperationContext context = contexts.get(CacheableOperation.class).iterator().next();
  			if (isConditionPassing(context, CacheOperationExpressionEvaluator.NO_RESULT)) {
  				Object key = generateKey(context, CacheOperationExpressionEvaluator.NO_RESULT);
  				Cache cache = context.getCaches().iterator().next();
  				try {
                      // 因为只有@Cacheable才有这个限制  直接查询出来后进行缓存,然后返回就可
                      //  cache.get 是spring封装的方法,返回此缓存映射指定键的值，如有必要，从vcallable获取该值。 
                      //  此方法为传统的“如果缓存，则返回；否则创建，缓存并返回”模式提供了简单的替代。
  					return wrapCacheValue(method, cache.get(key, new Callable<Object>() {
  						@Override
  						public Object call() throws Exception {
  							return unwrapReturnValue(invokeOperation(invoker));
  						}
  					}));
  				}
  				catch (Cache.ValueRetrievalException ex) {
  					// The invoker wraps any Throwable in a ThrowableWrapper instance so we
  					// can just make sure that one bubbles up the stack.
  					throw (CacheOperationInvoker.ThrowableWrapper) ex.getCause();
  				}
  			}
  			else {
                  // 不满足条件直接返回原值
  				// No caching required, only call the underlying method
  				return invokeOperation(invoker);
  			}
  		}
      
  		// Process any early evictions
          // 处理缓存清除注解的逻辑
      	// 这里处理的是@CacheEvict(beforeInvocation = true)注解
  		processCacheEvicts(contexts.get(CacheEvictOperation.class), true,
  				CacheOperationExpressionEvaluator.NO_RESULT);
  
  		// Check if we have a cached item matching the conditions
          // 检查是否有指定的缓存
  		Cache.ValueWrapper cacheHit = findCachedItem(contexts.get(CacheableOperation.class));
  		
  		// Collect puts from any @Cacheable miss, if no cached item is found
  		List<CachePutRequest> cachePutRequests = new LinkedList<CachePutRequest>();
  		if (cacheHit == null) {
  			collectPutRequests(contexts.get(CacheableOperation.class),
  					CacheOperationExpressionEvaluator.NO_RESULT, cachePutRequests);
  		}
  
  		Object cacheValue;
  		Object returnValue;
  		
  		if (cacheHit != null && cachePutRequests.isEmpty() && !hasCachePut(contexts)) {
  			// If there are no put requests, just use the cache hit
  			cacheValue = cacheHit.get();
  			returnValue = wrapCacheValue(method, cacheValue);
  		}
  		else {
              // 执行原方法
  			// Invoke the method if we don't have a cache hit
  			returnValue = invokeOperation(invoker);
  			cacheValue = unwrapReturnValue(returnValue);
  		}
  
  		// Collect any explicit @CachePuts
  		collectPutRequests(contexts.get(CachePutOperation.class), cacheValue, cachePutRequests);
  
  		// Process any collected put requests, either from @CachePut or a @Cacheable miss
  		for (CachePutRequest cachePutRequest : cachePutRequests) {
  			cachePutRequest.apply(cacheValue);
  		}
  
  		// Process any late evictions
  		processCacheEvicts(contexts.get(CacheEvictOperation.class), false, cacheValue);
  
  		return returnValue;
  	}
  ```

  - 缓存清除时遇见的坑
    当执行`@CacheEvict`的时候, 如果使用了`allEntries = true`的属性可能会抛出异常,这是因为`spring-data-redis`2.2.0 - 2.6.0之间的版本都是使用的keys进行的批量获取key

  ```java
    	try {
            	   if (isLockingCacheWriter()) {
    					doLock(name, connection);
    					wasLocked = true;
    				}
    				// 使用的keys
    				byte[][] keys = Optional.ofNullable(connection.keys(pattern)).orElse(Collections.emptySet())
    						.toArray(new byte[0][]);
    
    				if (keys.length > 0) {
    					connection.del(keys);
    				}
    			} finally {
    
    				if (wasLocked && isLockingCacheWriter()) {
    					doUnlock(name, connection);
    				}
    			}
  ```

  而在很多公司的redis使用上,会主动禁用这个操作,导致抛出异常,而在2.6.0之后的版本上可以自主选择批量的策略,使用`scan`命令来获取所有的key.

总的来说,springCache使用上比较简单,强力推荐.几个具体的cache后面有时间可更为详细的分析下


