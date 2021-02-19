## spring Enviroment 初始化及@value加载

详细解析下配置的加载过程,一遍加深印象

源码解析思路来自[这篇文章](https://www.cnblogs.com/wuzhenzhao/p/13708308.html),说的很全面

### @value加载

`ConfigurableApplicationContext` 就是我们所创建的抽象的ioc容器,启动流程不太讲,对创建出的bean进行初始化处理的时候,会将各个注解转换成对应的bean注入,下面是bean获取源码

```java
	protected <T> T doGetBean(final String name, @Nullable final Class<T> requiredType,
			@Nullable final Object[] args, boolean typeCheckOnly) throws BeansException {
                //别名bean转成规范名称的bean 
		final String beanName = transformedBeanName(name);
		Object bean;
		//检查缓存中是不是已经有该单例bean
		//返回以给定名称注册的（原始）单例对象。 
		//检查已实例化的单例，并允许早期引用当前创建的单例（解析循环引用)
		// Eagerly check singleton cache for manually registered singletons.
		Object sharedInstance = getSingleton(beanName);
		if (sharedInstance != null && args == null) {
			if (logger.isTraceEnabled()) {
				if (isSingletonCurrentlyInCreation(beanName)) {
					logger.trace("Returning eagerly cached instance of singleton bean '" + beanName +
							"' that is not fully initialized yet - a consequence of a circular reference");
				}
				else {
					logger.trace("Returning cached instance of singleton bean '" + beanName + "'");
				}
			}
			// 获取该bean实例,主要是用来完成factorybean的处理
			// 再者就是将别名的bean指向规范生成的bean
			bean = getObjectForBeanInstance(sharedInstance, name, beanName, null);
		}

		else {
			// 会在当前在创建的bean 中查找这个bean名称
			// 查看线程私有的name,如果和当前创建的bean 名称一致
			// 说明在循环创建bean
			// Fail if we're already creating this bean instance:
			// We're assumably within a circular reference.
			if (isPrototypeCurrentlyInCreation(beanName)) {
				throw new BeanCurrentlyInCreationException(beanName);
			}

			// Check if bean definition exists in this factory.
			//检查当前bean定义是不是在当前beanfactory中
			// 注意这里是beanFactory, 和上文提到的factorybean不一样
			BeanFactory parentBeanFactory = getParentBeanFactory();
			// 如果当前bean定义 不存在,就去父类bean工厂找
			if (parentBeanFactory != null && !containsBeanDefinition(beanName)) {
				// Not found -> check parent.
				String nameToLookup = originalBeanName(name);
				if (parentBeanFactory instanceof AbstractBeanFactory) {
					return ((AbstractBeanFactory) parentBeanFactory).doGetBean(
							nameToLookup, requiredType, args, typeCheckOnly);
				}
				else if (args != null) {
					// Delegation to parent with explicit args.
					return (T) parentBeanFactory.getBean(nameToLookup, args);
				}
				else if (requiredType != null) {
					// No args -> delegate to standard getBean method.
					return parentBeanFactory.getBean(nameToLookup, requiredType);
				}
				else {
					return (T) parentBeanFactory.getBean(nameToLookup);
				}
			}
			//判断调用该bean的用处是啥,如果是为了创建
			//就将该bean移动到已创建的set中 
			if (!typeCheckOnly) {
				markBeanAsCreated(beanName);
			}

			try {
				// 获取bean的定义 并开始检查
				final RootBeanDefinition mbd = getMergedLocalBeanDefinition(beanName);
				checkMergedBeanDefinition(mbd, beanName, args);

				// Guarantee initialization of beans that the current bean depends on.
				//获取当前bean 所有依赖的bean的名称
				String[] dependsOn = mbd.getDependsOn();
				if (dependsOn != null) {
					for (String dep : dependsOn) {
						//排除循环依赖的情况
						if (isDependent(beanName, dep)) {
							throw new BeanCreationException(mbd.getResourceDescription(), beanName,
									"Circular depends-on relationship between '" + beanName + "' and '" + dep + "'");
						}
						//为指定bean注册一个 depends bean  并在该bean销毁前销毁depends bean
						registerDependentBean(dep, beanName);
						try {
							// 获取依赖bean
							getBean(dep);
						}
						catch (NoSuchBeanDefinitionException ex) {
							throw new BeanCreationException(mbd.getResourceDescription(), beanName,
									"'" + beanName + "' depends on missing bean '" + dep + "'", ex);
						}
					}
				}

				// Create bean instance.
				//开始创建bean
				// 判断该bean是单例还是多例
				if (mbd.isSingleton()) {
					sharedInstance = getSingleton(beanName, () -> {
						try {
							// 开始创建bean
							return createBean(beanName, mbd, args);
						}
						catch (BeansException ex) {
							// Explicitly remove instance from singleton cache: It might have been put there
							// eagerly by the creation process, to allow for circular reference resolution.
							// Also remove any beans that received a temporary reference to the bean.
							// 从单例模式bean 删除实例对象
							destroySingleton(beanName);
							throw ex;
						}
					});
					//将刚刚创建的bean 传递给当前的bean实例
					bean = getObjectForBeanInstance(sharedInstance, name, beanName, mbd);
				}

				else if (mbd.isPrototype()) {
					// It's a prototype -> create a new instance.
					//原型 模式 创建一个新的对象
					Object prototypeInstance = null;
					try {	
						// 创建bean的  NameThreadloacl中 添加当前创建的beanName
						beforePrototypeCreation(beanName);
						prototypeInstance = createBean(beanName, mbd, args);
					}
					finally {
						// 创建bean时  nameThreadLocal中 移除当前在创建的bean
						afterPrototypeCreation(beanName);
					}
					bean = getObjectForBeanInstance(prototypeInstance, name, beanName, mbd);
				}
				//要创建的Bean 既不是单例模式，也不是原型模式，则根据Bean 定义资源中
                		//配置的生命周期范围，选择实例化Bean 的合适方法，这种在Web 应用程序中
                		//比较常用，如：request、session、application 等生命周期
				else {
					String scopeName = mbd.getScope();
					final Scope scope = this.scopes.get(scopeName);
					if (scope == null) {
						throw new IllegalStateException("No Scope registered for scope name '" + scopeName + "'");
					}
					try {
						Object scopedInstance = scope.get(beanName, () -> {
							beforePrototypeCreation(beanName);
							try {
								return createBean(beanName, mbd, args);
							}
							finally {
								afterPrototypeCreation(beanName);
							}
						});
						bean = getObjectForBeanInstance(scopedInstance, name, beanName, mbd);
					}
					catch (IllegalStateException ex) {
						throw new BeanCreationException(beanName,
								"Scope '" + scopeName + "' is not active for the current thread; consider " +
								"defining a scoped proxy for this bean if you intend to refer to it from a singleton",
								ex);
					}
				}
			}
			catch (BeansException ex) {
				// 如果出现异常将当前bean 移除出已创建的list中
				cleanupAfterBeanCreationFailure(beanName);
				throw ex;
			}
		}

		// Check if required type matches the type of the actual bean instance.
		// 对创建好的bean进行类型检查
		if (requiredType != null && !requiredType.isInstance(bean)) {
			try {
				T convertedBean = getTypeConverter().convertIfNecessary(bean, requiredType);
				if (convertedBean == null) {
					throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getClass());
				}
				return convertedBean;
			}
			catch (TypeMismatchException ex) {
				if (logger.isTraceEnabled()) {
					logger.trace("Failed to convert bean '" + name + "' to required type '" +
							ClassUtils.getQualifiedName(requiredType) + "'", ex);
				}
				throw new BeanNotOfRequiredTypeException(name, requiredType, bean.getClass());
			}
		}
		return (T) bean;
	}


```

然后使用createBean来创建对象

```java
protected Object createBean(String beanName, RootBeanDefinition mbd, @Nullable Object[] args)
	throws BeanCreationException {

		if (logger.isTraceEnabled()) {
            logger.trace("Creating instance of bean '" + beanName + "'");
        
		}
	
        RootBeanDefinition mbdToUse = mbd;

        // Make sure bean class is actually resolved at this point, and
        // clone the bean definition in case of a dynamically resolved Class
        // which cannot be stored in the shared merged bean definition.
	//确保此时确实解析了bean类，
	//如果动态解析的Class 
	//无法存储在共享的合并bean定义中，则
	//复制bean定义
        Class<?> resolvedClass = resolveBeanClass(mbd, beanName);
	if (resolvedClass != null && !mbd.hasBeanClass() && mbd.getBeanClassName() != null) {
            mbdToUse = new RootBeanDefinition(mbd);
            mbdToUse.setBeanClass(resolvedClass);
	}

        // Prepare method overrides.
	// 准备bean中的重写方法
	try {
            mbdToUse.prepareMethodOverrides();
        
	}
	catch (BeanDefinitionValidationException ex) {
            throw new BeanDefinitionStoreException(mbdToUse.getResourceDescription(),
                    beanName, "Validation of method overrides failed", ex);
        
	}

	try {
            // Give BeanPostProcessors a chance to return a proxy instead of the target bean instance.
		//如果该bean有前置处理器或者后置处理器,就生成对应bean的代理对象
            Object bean = resolveBeforeInstantiation(beanName, mbdToUse);
	    if (bean != null) {
                return bean;
            
	    }
        
	}
	catch (Throwable ex) {
            throw new BeanCreationException(mbdToUse.getResourceDescription(), beanName,
                    "BeanPostProcessor before instantiation of bean failed", ex);
        
	}

	try {
		//开始创建bean
            Object beanInstance = doCreateBean(beanName, mbdToUse, args);
	    if (logger.isTraceEnabled()) {
                logger.trace("Finished creating instance of bean '" + beanName + "'");
            
	    }
            return beanInstance;
        
	}
	catch (BeanCreationException | ImplicitlyAppearedSingletonException ex) {
            // A previously detected exception with proper bean creation context already,
            // or illegal singleton state to be communicated up to DefaultSingletonBeanRegistry.
            throw ex;
        
	}
	catch (Throwable ex) {
		throw new BeanCreationException(
                    mbdToUse.getResourceDescription(), beanName, "Unexpected exception during bean creation", ex
				);
        
	}    
}
```

开始调用`doGetBean` 真正开始创建对应的bean

```java
protected Object doCreateBean(final String beanName, final RootBeanDefinition mbd, final @Nullable Object[] args)
	throws BeanCreationException {

        // Instantiate the bean.
        BeanWrapper instanceWrapper = null;
	if (mbd.isSingleton()) {
            instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
        
	}
	if (instanceWrapper == null) {
            instanceWrapper = createBeanInstance(beanName, mbd, args);
        
	}
        final Object bean = instanceWrapper.getWrappedInstance();
        Class<?> beanType = instanceWrapper.getWrappedClass();
	if (beanType != NullBean.class) {
            mbd.resolvedTargetType = beanType;
        
	}

        // Allow post-processors to modify the merged bean definition.
	synchronized (mbd.postProcessingLock) {
		if (!mbd.postProcessed) {
			try {
                    applyMergedBeanDefinitionPostProcessors(mbd, beanType, beanName);
                
			}
			catch (Throwable ex) {
                    throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                            "Post-processing of merged bean definition failed", ex);
                
			}
                mbd.postProcessed = true;
            
		}
        
	}

        // Eagerly cache singletons to be able to resolve circular references
        // even when triggered by lifecycle interfaces like BeanFactoryAware.
        boolean earlySingletonExposure = (mbd.isSingleton() && this.allowCircularReferences &&
                isSingletonCurrentlyInCreation(beanName));
	if (earlySingletonExposure) {
		if (logger.isTraceEnabled()) {
                logger.trace("Eagerly caching bean '" + beanName +
                        "' to allow for resolving potential circular references");
            
		}
            addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
        
	}

        // Initialize the bean instance.
        Object exposedObject = bean;
	try {
            populateBean(beanName, mbd, instanceWrapper);
            exposedObject = initializeBean(beanName, exposedObject, mbd);
        
	}
	catch (Throwable ex) {
		if (ex instanceof BeanCreationException && beanName.equals(((BeanCreationException) ex).getBeanName())) {
                throw (BeanCreationException) ex;
            
		}
		else {
			throw new BeanCreationException(
                        mbd.getResourceDescription(), beanName, "Initialization of bean failed", ex
					);
            
		}
        
	}

	if (earlySingletonExposure) {
            Object earlySingletonReference = getSingleton(beanName, false);
	    if (earlySingletonReference != null) {
		    if (exposedObject == bean) {
                    exposedObject = earlySingletonReference;
                
		    }
		    else if (!this.allowRawInjectionDespiteWrapping && hasDependentBean(beanName)) {
                    String[] dependentBeans = getDependentBeans(beanName);
                    Set<String> actualDependentBeans = new LinkedHashSet<>(dependentBeans.length);
		    for (String dependentBean : dependentBeans) {
			    if (!removeSingletonIfCreatedForTypeCheckOnly(dependentBean)) {
                            actualDependentBeans.add(dependentBean);
                        
			    }
                    
		    }
		    if (!actualDependentBeans.isEmpty()) {
                        throw new BeanCurrentlyInCreationException(beanName,
                                "Bean with name '" + beanName + "' has been injected into other beans [" +
                                StringUtils.collectionToCommaDelimitedString(actualDependentBeans) +
                                "] in its raw version as part of a circular reference, but has eventually been " +
                                "wrapped. This means that said other beans do not use the final version of the " +
                                "bean. This is often the result of over-eager type matching - consider using " +
                                "'getBeanNamesForType' with the 'allowEagerInit' flag turned off, for example.");
                    
		    }
                
		    }
            
	    }
        
	}

        // Register bean as disposable.
	try {
            registerDisposableBeanIfNecessary(beanName, bean, mbd);
        
	}
	catch (BeanDefinitionValidationException ex) {
		throw new BeanCreationException(
                    mbd.getResourceDescription(), beanName, "Invalid destruction signature", ex
				);
        
	}

        return exposedObject;
    
	}

```

