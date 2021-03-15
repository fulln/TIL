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
	   //如果是单例,就需要在工厂bean中删除缓存,并获取到这个bean	
            instanceWrapper = this.factoryBeanInstanceCache.remove(beanName);
        
	}
	if (instanceWrapper == null) {
	   //如果发现之前没有创建,就开始创建beanwapper对象
            instanceWrapper = createBeanInstance(beanName, mbd, args);
        
	}
        final Object bean = instanceWrapper.getWrappedInstance();
        Class<?> beanType = instanceWrapper.getWrappedClass();
	//开始设置bean的类型
	if (beanType != NullBean.class) {
            mbd.resolvedTargetType = beanType;
        
	}

        // Allow post-processors to modify the merged bean definition.
	// 开始使用后置处理器
	synchronized (mbd.postProcessingLock) {
		if (!mbd.postProcessed) {
			try {
			//
                    applyMergedBeanDefinitionPostProcessors(mbd, beanType, beanName);
                
			}
			catch (Throwable ex) {
                    throw new BeanCreationException(mbd.getResourceDescription(), beanName,
                            "Post-processing of merged bean definition failed", ex);
                
			}
                mbd.postProcessed = true;
            
		}
        
	}
	//缓存bean对象,防止循环引用
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
	//开始初始化bean.依赖注入就是在这里触发
	//这个exposedObject 在初始化完成之后返回作为依赖注入完成后的Bean
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
	//缓存与否
	if (earlySingletonExposure) {
		// 获取指定名称的bean单例对象
            Object earlySingletonReference = getSingleton(beanName, false);
	    if (earlySingletonReference != null) {
		// 发现是同一个对象的话,就返回这个
		    if (exposedObject == bean) {
                    exposedObject = earlySingletonReference;
                
		    }
			// 发现bean依赖 其他bean,并且有循环引用不能注册对象时
		    else if (!this.allowRawInjectionDespiteWrapping && hasDependentBean(beanName)) {
			// 获取当前bean 依赖的其他所有bean
                    String[] dependentBeans = getDependentBeans(beanName);
                    Set<String> actualDependentBeans = new LinkedHashSet<>(dependentBeans.length);
		    for (String dependentBean : dependentBeans) {
				//进行类型检查, 主要检查有没有被创建, 创建过的就提示报错
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
	// 注册这个完成依赖注入的bean
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
 可以看出,依赖bean的注入主要在populateBean 和createBeanInstance 这2个方法里面,开始分析`createBeanINstance`

```java
protected BeanWrapper createBeanInstance(String beanName, RootBeanDefinition mbd, @Nullable Object[] args) {
		// Make sure bean class is actually resolved at this point.
		//确认bean这里是可以被实例化的
		Class<?> beanClass = resolveBeanClass(mbd, beanName);

		if (beanClass != null && !Modifier.isPublic(beanClass.getModifiers()) && !mbd.isNonPublicAccessAllowed()) {
			throw new BeanCreationException(mbd.getResourceDescription(), beanName,
					"Bean class isn't public, and non-public access not allowed: " + beanClass.getName());
		}
		
		Supplier<?> instanceSupplier = mbd.getInstanceSupplier();
		if (instanceSupplier != null) {
			return obtainFromSupplier(instanceSupplier, beanName);
		}
		// 发现这个bean可以被工厂bean初始化,就直接用这个工厂bean返回的实例
		if (mbd.getFactoryMethodName() != null) {
			return instantiateUsingFactoryMethod(beanName, mbd, args);
		}

		// Shortcut when re-creating the same bean...
		// 重复创建相同的bean的时候就可以使用下面的方法,快速进行创建
		boolean resolved = false;
		boolean autowireNecessary = false;
		if (args == null) {
			synchronized (mbd.constructorArgumentLock) {
				//看下之前创建bean 的时候 有没有需要对应的依赖bean注入
				if (mbd.resolvedConstructorOrFactoryMethod != null) {
					resolved = true;
					autowireNecessary = mbd.constructorArgumentsResolved;
				}
			}
		}
		if (resolved) {
			if (autowireNecessary) {
				//使用构造方法注入的形式 注入对应bean
				return autowireConstructor(beanName, mbd, null, null);
			}
			else {
				// 使用了无参的方法进行构造
				return instantiateBean(beanName, mbd);
			}
		}

		// Candidate constructors for autowiring?
		Constructor<?>[] ctors = determineConstructorsFromBeanPostProcessors(beanClass, beanName);
		if (ctors != null || mbd.getResolvedAutowireMode() == AUTOWIRE_CONSTRUCTOR ||
				mbd.hasConstructorArgumentValues() || !ObjectUtils.isEmpty(args)) {
			/使用容器的自动装配特性，调用匹配的构造方法实例化
			return autowireConstructor(beanName, mbd, ctors, args);
		}

		// Preferred constructors for default construction?
		ctors = mbd.getPreferredConstructors();
		// 使用bean的有参构造方法初始化bean
		if (ctors != null) {
			return autowireConstructor(beanName, mbd, ctors, null);
		}
		// 使用默认的无参构造防范
		// No special handling: simply use no-arg constructor.
		return instantiateBean(beanName, mbd);
	}

protected BeanWrapper instantiateBean(final String beanName, final RootBeanDefinition mbd) {
		try {
			Object beanInstance;
			final BeanFactory parent = this;
			if (System.getSecurityManager() != null) {
				//根据实例策略创建对应的对象
				beanInstance = AccessController.doPrivileged((PrivilegedAction<Objct>) () ->
						getInstantiationStrategy().instantiate(mbd, beanName, parent),
						getAccessControlContext());
			}
			else {
				//开始封装对应的实例
				beanInstance = getInstantiationStrategy().instantiate(mbd, beanName, parent);
			}
			BeanWrapper bw = new BeanWrapperImpl(beanInstance);
			initBeanWrapper(bw);
			return bw;
		}
		catch (Throwable ex) {
			throw new BeanCreationException(
					mbd.getResourceDescription(), beanName, "Instantiation of bean failed", ex);
		}
}
```
执行bean实例化

在使用默认的无参构造方法创建Bean 的实例化对象时，方法getInstantiationStrategy().instantiate()调用了SimpleInstantiationStrategy 类中的实例化Bean 的方法，其源码如下：

```java
@Override
public Object instantiate(RootBeanDefinition bd, @Nullable String beanName, BeanFactory owner) {
        // Don't override the class with CGLIB if no overrides.
	//如果没有说需要重写  就不要用cglib重写
	if (!bd.hasMethodOverrides()) {
            Constructor<?> constructorToUse;
	    synchronized (bd.constructorArgumentLock) {
                constructorToUse = (Constructor<?>) bd.resolvedConstructorOrFactoryMethod;
		if (constructorToUse == null) {
                    final Class<?> clazz = bd.getBeanClass();
		    if (clazz.isInterface()) {
                        throw new BeanInstantiationException(clazz, "Specified class is an interface");
                    
		    }
		    try {
			    if (System.getSecurityManager() != null) {
				//如果开启了严格保护系统, 用security的方式 开始获取构造,
				    constructorToUse = AccessController.doPrivileged(
                                    (PrivilegedExceptionAction<Constructor<?>>) clazz::getDeclaredConstructor
						    );
                        
			    }
			    else {
				//直接获取构造方法
                            constructorToUse = clazz.getDeclaredConstructor();
                        
			    }
                        bd.resolvedConstructorOrFactoryMethod = constructorToUse;
                    
		    }
		    catch (Throwable ex) {
                        throw new BeanInstantiationException(clazz, "No default constructor found", ex);
                    
		    }
                
		}
            
	    }
		//  使用beanutils实例话,反射执行对应的构造方法
            return BeanUtils.instantiateClass(constructorToUse);
        
	}
	else {
	// 必须用cglib进行方法重写
            // Must generate CGLIB subclass.
            return instantiateWithMethodInjection(bd, beanName, owner);
        
	}
    
}
```

这里还有个`@CallerSensitive` 的注解,baidu了下  发现这个注解只是会出现在jvm内部,而且主要作用,我引用下其他人的发言

```
这个注解是为了堵住漏洞用的。曾经有黑客通过构造双重反射来提升权限，原理是当时反射只检查固定深度的调用者的类，看它有没有特权，例如固定看两层的调用者（getCallerClass(2)）。如果我的类本来没足够权限群访问某些信息，那我就可以通过双重反射去达到目的：反射相关的类是有很高权限的，而在 我->反射1->反射2 这样的调用链上，反射2检查权限时看到的是反射1的类，这就被欺骗了，导致安全漏洞。使用CallerSensitive后，getCallerClass不再用固定深度去寻找actual caller（“我”），而是把所有跟反射相关的接口方法都标注上CallerSensitive，搜索时凡看到该注解都直接跳过，这样就有效解决了前面举例的问题
```

### 准备依赖注入

在创建完bean实例之后,并不是说就弄完, 获取到实例之后, 会去先看下这个bean相关的后置处理器,缓存当前单例实例以便循环解析使用,然后再初始化这个bean实例里面的成员,下面方法就是初始化成员的地方

```java

protected void populateBean(String beanName, RootBeanDefinition mbd, @Nullable BeanWrapper bw) {
	// 非空的判断
	if (bw == null) {
		if (mbd.hasPropertyValues()) {
			throw new BeanCreationException(
                        mbd.getResourceDescription(), beanName, "Cannot apply property values to null instance"
					);
            
		}
		else {
                // Skip property population phase for null instance.
                return;
            
		}
        
	}

        // Give any InstantiationAwareBeanPostProcessors the opportunity to modify the
        // state of the bean before properties are set. This can be used, for example,
        // to support styles of field injection.
	//给任何实例化awarebeanpostprocessor在属性设置之前修改bean状态的机会。例如，这可以用来支持字段注入的样式。
	if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
		for (BeanPostProcessor bp : getBeanPostProcessors()) {
			if (bp instanceof InstantiationAwareBeanPostProcessor) {
                    InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
		    if (!ibp.postProcessAfterInstantiation(bw.getWrappedInstance(), beanName)) {
                        return;
                    
		    }
                
			}
            
		}
        
	}
	//获取在bean定义的时候创建的配置属性值
        PropertyValues pvs = (mbd.hasPropertyValues() ? mbd.getPropertyValues() : null);

        int resolvedAutowireMode = mbd.getResolvedAutowireMode();
	//根据名称或者是class类型注入bean 
	if (resolvedAutowireMode == AUTOWIRE_BY_NAME || resolvedAutowireMode == AUTOWIRE_BY_TYPE) {
            MutablePropertyValues newPvs = new MutablePropertyValues(pvs);
            // Add property values based on autowire by name if applicable.
	    if (resolvedAutowireMode == AUTOWIRE_BY_NAME) {
                autowireByName(beanName, mbd, bw, newPvs);
            
	    }
            // Add property values based on autowire by type if applicable.
	    if (resolvedAutowireMode == AUTOWIRE_BY_TYPE) {
                autowireByType(beanName, mbd, bw, newPvs);
            
	    }
            pvs = newPvs;
        
	}
	//判断有没有bean的后置处理器	
        boolean hasInstAwareBpps = hasInstantiationAwareBeanPostProcessors();
	// 判断需要深层次检查
        boolean needsDepCheck = (mbd.getDependencyCheck() != AbstractBeanDefinition.DEPENDENCY_CHECK_NONE);

        PropertyDescriptor[] filteredPds = null;
	if (hasInstAwareBpps) {
		if (pvs == null) {
                pvs = mbd.getPropertyValues();
            
		}
		//构建bean的后置处理器对bean处理
		for (BeanPostProcessor bp : getBeanPostProcessors()) {
			if (bp instanceof InstantiationAwareBeanPostProcessor) {
                    InstantiationAwareBeanPostProcessor ibp = (InstantiationAwareBeanPostProcessor) bp;
                    PropertyValues pvsToUse = ibp.postProcessProperties(pvs, bw.getWrappedInstance(), beanName);
		    if (pvsToUse == null) {
			    if (filteredPds == null) {
                            filteredPds = filterPropertyDescriptorsForDependencyCheck(bw, mbd.allowCaching);
                        
			    }
                        pvsToUse = ibp.postProcessPropertyValues(pvs, filteredPds, bw.getWrappedInstance(), beanName);
			if (pvsToUse == null) {
                            return;
                        
			}
                    
		    }
                    pvs = pvsToUse;
                
			}
            
		}
        
	}
	if (needsDepCheck) {
		if (filteredPds == null) {
                filteredPds = filterPropertyDescriptorsForDependencyCheck(bw, mbd.allowCaching);
            
		}
            checkDependencies(beanName, mbd, filteredPds, pvs);
        
	}
	//属性输入
	if (pvs != null) {
            applyPropertyValues(beanName, mbd, bw, pvs);
        
	}
    
}

//应用给定的属性值，将所有运行时引用解析为该bean工厂中的其他bean。必须使用深层复制，因此我们不会永久修改此属性。
protected void applyPropertyValues(String beanName, BeanDefinition mbd, BeanWrapper bw, PropertyValues pvs) {
		if (pvs.isEmpty()) {
			return;
		}

		if (System.getSecurityManager() != null && bw instanceof BeanWrapperImpl) {
			((BeanWrapperImpl) bw).setSecurityContext(getAccessControlContext());
		}
		//多属性处理
		MutablePropertyValues mpvs = null;
		List<PropertyValue> original;

		if (pvs instanceof MutablePropertyValues) {
			mpvs = (MutablePropertyValues) pvs;
			if (mpvs.isConverted()) {
				// Shortcut: use the pre-converted values as-is.
				try {
					//直接设置好参数返回
					bw.setPropertyValues(mpvs);
					return;
				}
				catch (BeansException ex) {
					throw new BeanCreationException(
							mbd.getResourceDescription(), beanName, "Error setting property values", ex);
				}
			}
			//获取对象的原始类型值 list
			original = mpvs.getPropertyValueList();
		}
		else {
			original = Arrays.asList(pvs.getPropertyValues());
		}
		//用户自定义转换
		TypeConverter converter = getCustomTypeConverter();
		if (converter == null) {
			converter = bw;
		}
		//创建bean的定义解析器, 将bean中定义的属性解析成实际对象值
		BeanDefinitionValueResolver valueResolver = new BeanDefinitionValueResolver(this, beanName, mbd, converter);

		// Create a deep copy, resolving any references for values.
		List<PropertyValue> deepCopy = new ArrayList<>(original.size());
		boolean resolveNecessary = false;
		
		for (PropertyValue pv : original) {
			//已经转换了的
			if (pv.isConverted()) {
				deepCopy.add(pv);
			}
			else {
			// 未转换的
				String propertyName = pv.getName();
				//原始属性值
				Object originalValue = pv.getValue();
				if (originalValue == AutowiredPropertyMarker.INSTANCE) {
					Method writeMethod = bw.getPropertyDescriptor(propertyName).getWriteMethod();
					if (writeMethod == null) {
						throw new IllegalArgumentException("Autowire marker for property without write method: " + pv);
					}
					originalValue = new DependencyDescriptor(new MethodParameter(writeMethod, 0), true);
				}
				Object resolvedValue = valueResolver.resolveValueIfNecessary(pv, originalValue);
				Object convertedValue = resolvedValue;
				boolean convertible = bw.isWritableProperty(propertyName) &&
						!PropertyAccessorUtils.isNestedOrIndexedProperty(propertyName);
				if (convertible) {
					convertedValue = convertForProperty(resolvedValue, propertyName, bw, converter);
				}
				// Possibly store converted value in merged bean definition,
				// in order to avoid re-conversion for every created bean instance.
				if (resolvedValue == originalValue) {
					if (convertible) {
						pv.setConvertedValue(convertedValue);
					}
					deepCopy.add(pv);
				}
				else if (convertible && originalValue instanceof TypedStringValue &&
						!((TypedStringValue) originalValue).isDynamic() &&
						!(convertedValue instanceof Collection || ObjectUtils.isArray(convertedValue))) {
					pv.setConvertedValue(convertedValue);
					deepCopy.add(pv);
				}
				else {
					resolveNecessary = true;
					deepCopy.add(new PropertyValue(pv, convertedValue));
				}
			}
		}
		if (mpvs != null && !resolveNecessary) {
			mpvs.setConverted();
		}

		// Set our (possibly massaged) deep copy.
		try {
			bw.setPropertyValues(new MutablePropertyValues(deepCopy));
		}
		catch (BeansException ex) {
			throw new BeanCreationException(
					mbd.getResourceDescription(), beanName, "Error setting property values", ex);
		}
	}

```



