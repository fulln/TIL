#java #spring #log

## SpringMVC全局日志	

### 简介

在业务开发过程中, 一般会要求记录比较详细的日志的输入,下面总结了几点比较常见的方式

* 使用`Intecepter`拦截到request的请求, 然后对请求进行日志的记录
* 使用`AOP`拦截,通常会伴随着异常的拦截和统一返回.一般表现形式会使用注解
* 使用`RequestBodyAdviceAdapter`等spring自带的拦截进行处理

大部分人都是选择的以上的2点,但是今天主要是说用第三点来处理这个日志.

### 使用方法

#### 创建 `AdviceHandle`

```java
package com.log.helper.advice;

import com.alibaba.fastjson.JSON;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.MethodParameter;
import org.springframework.http.HttpInputMessage;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.servlet.mvc.method.annotation.RequestBodyAdviceAdapter;

import javax.servlet.http.HttpServletRequest;
import java.lang.reflect.Type;

/**
 * @author fulln
 * @version 0.0.1
 * @program logHelper
 * @description advice handle
 * @date 2021/7/4 15:25
 **/
@Slf4j
@RestControllerAdvice
public class RestControllerAdviceHandle extends RequestBodyAdviceAdapter {

    /**
     * 日志打印
     * @param body 入参
     */
    public void setLog(Object body) {
        HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
        //仅仅打印请求参数
        String s = JSON.toJSONString(body);
        // 打印日志
        log.info("请求路径：" + request.getRequestURI() + ",参数" + s);
    }

    @Override
    public boolean supports(MethodParameter methodParameter, Type targetType, Class<? extends HttpMessageConverter<?>> converterType) {
        return true;
    }

    @Override
    public Object handleEmptyBody(Object body, HttpInputMessage inputMessage, MethodParameter parameter, Type targetType, Class<? extends HttpMessageConverter<?>> converterType) {
        setLog(null);
        return body;
    }

    @Override
    public Object afterBodyRead(Object body, HttpInputMessage inputMessage, MethodParameter parameter, Type targetType, Class<? extends HttpMessageConverter<?>> converterType) {
        setLog(body);
        return body;
    }


}

```

 这样就能拦截所有带有`RequestBody`的请求入参,一般大部分值得拦截的入参都能拦截到,还有部分的请求可以直接打对应的日志来进行处理.

### 流程

![时序图](requesrBody.png)

可以看出,在1.9部分调用`afterBodyRead`,其主要调用方法是从`org.springframework.web.servlet.mvc.method.annotation.HttpEntityMethodProcessor#resolveArgument` 出发开始处理,在处理参数的时候手动加入`beforeBodyRead`和`afterBodyRead`,实现`aop`的相同功能

### 源码分析

首先看自动装配,我们引入了

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

这个web包,因此会去自动装配区加载以下配置

```java
org.springframework.boot.autoconfigure.web.servlet.WebMvcAutoConfiguration.AutoConfigureAfter=org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration,org.springframework.boot.autoconfigure.task.TaskExecutionAutoConfiguration,org.springframework.boot.autoconfigure.validation.ValidationAutoConfiguration
```



入口源码可以看到`springMVC`的还是使用的是在`org.springframework.web.servlet.DispatcherServlet#doDispatch`

```java
/**
	 * Process the actual dispatching to the handler.
	 * <p>The handler will be obtained by applying the servlet's HandlerMappings in order.
	 * The HandlerAdapter will be obtained by querying the servlet's installed HandlerAdapters
	 * to find the first that supports the handler class.
	 * <p>All HTTP methods are handled by this method. It's up to HandlerAdapters or handlers
	 * themselves to decide which methods are acceptable.
	 * @param request current HTTP request
	 * @param response current HTTP response
	 * @throws Exception in case of any kind of processing failure
	 */
	protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
				...
				//在实际上去处理对应请求
				mv = ha.handle(processedRequest, response, mappedHandler.getHandler());

				if (asyncManager.isConcurrentHandlingStarted()) {
					return;
				}

				...
	}
```

然后跳转到`org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter#handleInternal`去处理交互,这个里面就有对应的所有的请求连接

```java
protected ModelAndView handleInternal(HttpServletRequest request,
			HttpServletResponse response, HandlerMethod handlerMethod) throws Exception {

		ModelAndView mav;
		checkRequest(request);

		// 执行方法,在同步锁获取到的情况下
		if (this.synchronizeOnSession) {
			HttpSession session = request.getSession(false);
			if (session != null) {
				Object mutex = WebUtils.getSessionMutex(session);
				synchronized (mutex) {
					mav = invokeHandlerMethod(request, response, handlerMethod);
				}
			}
			else {
				//  HttpSession 可用,不需要互斥
				mav = invokeHandlerMethod(request, response, handlerMethod);
			}
		}
		else {
			// 不需要同步锁
			mav = invokeHandlerMethod(request, response, handlerMethod);
		}

		if (!response.containsHeader(HEADER_CACHE_CONTROL)) {
			if (getSessionAttributesHandler(handlerMethod).hasSessionAttributes()) {
				applyCacheSeconds(response, this.cacheSecondsForSessionAttributeHandlers);
			}
			else {
				prepareResponse(response);
			}
		}

		return mav;
	}
```

然后可以看到都调用了`invokeHandlerMethod` 方法,这个方法就是用`@requestMapping`来找到对应视图层`webmodel`,来展开进入这个方法

```java
protected ModelAndView invokeHandlerMethod(HttpServletRequest request,
			HttpServletResponse response, HandlerMethod handlerMethod) throws Exception {

		ServletWebRequest webRequest = new ServletWebRequest(request, response);
		try {
			...
			// 从modelfacatory中初始化对应的model,给对应model赋予对应的功能
			modelFactory.initModel(webRequest, mavContainer, invocableMethod);
			mavContainer.setIgnoreDefaultModelOnRedirect(this.ignoreDefaultModelOnRedirect);

			AsyncWebRequest asyncWebRequest = WebAsyncUtils.createAsyncWebRequest(request, response);
			asyncWebRequest.setTimeout(this.asyncRequestTimeout);

			WebAsyncManager asyncManager = WebAsyncUtils.getAsyncManager(request);
			asyncManager.setTaskExecutor(this.taskExecutor);
			asyncManager.setAsyncWebRequest(asyncWebRequest);
			asyncManager.registerCallableInterceptors(this.callableInterceptors);
			asyncManager.registerDeferredResultInterceptors(this.deferredResultInterceptors);

			if (asyncManager.hasConcurrentResult()) {
				Object result = asyncManager.getConcurrentResult();
				mavContainer = (ModelAndViewContainer) asyncManager.getConcurrentResultContext()[0];
				asyncManager.clearConcurrentResult();
				LogFormatUtils.traceDebug(logger, traceOn -> {
					String formatted = LogFormatUtils.formatValue(result, !traceOn);
					return "Resume with async result [" + formatted + "]";
				});
				invocableMethod = invocableMethod.wrapConcurrentResult(result);
			}

			invocableMethod.invokeAndHandle(webRequest, mavContainer);
			if (asyncManager.isConcurrentHandlingStarted()) {
				return null;
			}

			return getModelAndView(mavContainer, modelFactory, webRequest);
		}
		finally {
			webRequest.requestCompleted();
		}
	}
```

然后看到初始化Model时时调用的`initModel`方法,在这个方法中又掉`invokeModelAttributeMethods`来初始化model参数

```java
private void invokeModelAttributeMethods(NativeWebRequest request, ModelAndViewContainer container)
			throws Exception {

		while (!this.modelMethods.isEmpty()) {
			InvocableHandlerMethod modelMethod = getNextModelMethod(container).getHandlerMethod();
            // ModelAttribute 是在此使用,并注入到container中
			ModelAttribute ann = modelMethod.getMethodAnnotation(ModelAttribute.class);
			Assert.state(ann != null, "No ModelAttribute annotation");
			if (container.containsAttribute(ann.name())) {
				if (!ann.binding()) {
					container.setBindingDisabled(ann.name());
				}
				continue;
			}
			//在给定请求的上下文中解析其参数值后调用该方法。解析入参值
			//参数值通常通过HandlerMethodArgumentResolvers解析。
            //然而， providedArgs参数可以提供直接使用的参数值，即没有参数解析。
            //提供的参数值的示例包括WebDataBinder 、 SessionStatus或抛出的异常实例。
            //在参数解析器之前检查提供的参数值。
			//委托getMethodArgumentValues并使用解析的参数调用doInvoke 
			Object returnValue = modelMethod.invokeForRequest(request, container);
			if (modelMethod.isVoid()) {
				if (StringUtils.hasText(ann.value())) {
					if (logger.isDebugEnabled()) {
						logger.debug("Name in @ModelAttribute is ignored because method returns void: " +
								modelMethod.getShortLogMessage());
					}
				}
				continue;
			}
			//获取入参名称,绑定对应的key-value关系
			String returnValueName = getNameForReturnValue(returnValue, modelMethod.getReturnType());
			if (!ann.binding()) {
				container.setBindingDisabled(returnValueName);
			}
			if (!container.containsAttribute(returnValueName)) {
				container.addAttribute(returnValueName, returnValue);
			}
		}
	}
```

我们看到对应的入参解析方法`invokeForRequest`

```java
protected Object[] getMethodArgumentValues(NativeWebRequest request, @Nullable ModelAndViewContainer mavContainer,
			Object... providedArgs) throws Exception {

		MethodParameter[] parameters = getMethodParameters();
		if (ObjectUtils.isEmpty(parameters)) {
			return EMPTY_ARGS;
		}

		Object[] args = new Object[parameters.length];
		for (int i = 0; i < parameters.length; i++) {
			...
			try {
                // 针对resolvers 去处理不同的参数
				args[i] = this.resolvers.resolveArgument(parameter, mavContainer, request, this.dataBinderFactory);
			}
			catch (Exception ex) {
				// Leave stack trace for later, exception may actually be resolved and handled...
				if (logger.isDebugEnabled()) {
					String exMsg = ex.getMessage();
					if (exMsg != null && !exMsg.contains(parameter.getExecutable().toGenericString())) {
						logger.debug(formatArgumentError(parameter, exMsg));
					}
				}
				throw ex;
			}
		}
		return args;
	}
```

根据不同的处理器, 去处理对应的参数

```java
	public Object resolveArgument(MethodParameter parameter, @Nullable ModelAndViewContainer mavContainer,
			NativeWebRequest webRequest, @Nullable WebDataBinderFactory binderFactory) throws Exception {

		HandlerMethodArgumentResolver resolver = getArgumentResolver(parameter);
		if (resolver == null) {
			throw new IllegalArgumentException("Unsupported parameter type [" +
					parameter.getParameterType().getName() + "]. supportsParameter should be called first.");
		}
		return resolver.resolveArgument(parameter, mavContainer, webRequest, binderFactory);
	}
```

`requestBody`是到http实体处理类`HttpEntityMethodProcessor`,对参数进行处理

```java
public Object resolveArgument(MethodParameter parameter, @Nullable ModelAndViewContainer mavContainer,
			NativeWebRequest webRequest, @Nullable WebDataBinderFactory binderFactory)
			throws IOException, HttpMediaTypeNotSupportedException {
		//创建请求message
		ServletServerHttpRequest inputMessage = createInputMessage(webRequest);
		Type paramType = getHttpEntityType(parameter);
		if (paramType == null) {
			throw new IllegalArgumentException("HttpEntity parameter '" + parameter.getParameterName() +
					"' in method " + parameter.getMethod() + " is not parameterized");
		}
		//进行一个参数的自定义转换
		Object body = readWithMessageConverters(webRequest, parameter, paramType);
		if (RequestEntity.class == parameter.getParameterType()) {
			return new RequestEntity<>(body, inputMessage.getHeaders(),
					inputMessage.getMethod(), inputMessage.getURI());
		}
		else {
			return new HttpEntity<>(body, inputMessage.getHeaders());
		}
	}
```

看到,在对参数的处理中,会对参数进行自定义转换,

```java
protected <T> Object readWithMessageConverters(HttpInputMessage inputMessage, MethodParameter parameter,
			Type targetType) throws IOException, HttpMediaTypeNotSupportedException, HttpMessageNotReadableException {

		MediaType contentType;
		boolean noContentType = false;
		try {
			contentType = inputMessage.getHeaders().getContentType();
		}
		catch (InvalidMediaTypeException ex) {
			throw new HttpMediaTypeNotSupportedException(ex.getMessage());
		}
		if (contentType == null) {
			noContentType = true;
			contentType = MediaType.APPLICATION_OCTET_STREAM;
		}

		Class<?> contextClass = parameter.getContainingClass();
		Class<T> targetClass = (targetType instanceof Class ? (Class<T>) targetType : null);
		if (targetClass == null) {
			ResolvableType resolvableType = ResolvableType.forMethodParameter(parameter);
			targetClass = (Class<T>) resolvableType.resolve();
		}

		HttpMethod httpMethod = (inputMessage instanceof HttpRequest ? ((HttpRequest) inputMessage).getMethod() : null);
		Object body = NO_VALUE;

		EmptyBodyCheckingHttpInputMessage message;
		try {
			message = new EmptyBodyCheckingHttpInputMessage(inputMessage);

			for (HttpMessageConverter<?> converter : this.messageConverters) {
				Class<HttpMessageConverter<?>> converterType = (Class<HttpMessageConverter<?>>) converter.getClass();
				GenericHttpMessageConverter<?> genericConverter =
						(converter instanceof GenericHttpMessageConverter ? (GenericHttpMessageConverter<?>) converter : null);
				if (genericConverter != null ? genericConverter.canRead(targetType, contextClass, contentType) :
						(targetClass != null && converter.canRead(targetClass, contentType))) {
                    // 判断当前是不是有body的
					if (message.hasBody()) {
                        // 有就执行before 和after 的自定义方法 
						HttpInputMessage msgToUse =
								getAdvice().beforeBodyRead(message, parameter, targetType, converterType);
						body = (genericConverter != null ? genericConverter.read(targetType, contextClass, msgToUse) :
								((HttpMessageConverter<T>) converter).read(targetClass, msgToUse));
						body = getAdvice().afterBodyRead(body, msgToUse, parameter, targetType, converterType);
					}
					else {
                        //没有就执行空实体的自定义方法
						body = getAdvice().handleEmptyBody(null, message, parameter, targetType, converterType);
					}
					break;
				}
			}
		}
		catch (IOException ex) {
			throw new HttpMessageNotReadableException("I/O error while reading input message", ex, inputMessage);
		}

		if (body == NO_VALUE) {
			if (httpMethod == null || !SUPPORTED_METHODS.contains(httpMethod) ||
					(noContentType && !message.hasBody())) {
				return null;
			}
			throw new HttpMediaTypeNotSupportedException(contentType,
					getSupportedMediaTypes(targetClass != null ? targetClass : Object.class));
		}

		MediaType selectedContentType = contentType;
		Object theBody = body;
		LogFormatUtils.traceDebug(logger, traceOn -> {
			String formatted = LogFormatUtils.formatValue(theBody, !traceOn);
			return "Read \"" + selectedContentType + "\" to [" + formatted + "]";
		});

		return body;
	}
```



### 注意事项

1. `org.springframework.web.method.support.HandlerMethodArgumentResolver#resolveArgument` 有很多种对参数的解析processor,如入参的不需调用`readWithMessageConverters`,将执行不到自定义的日志拦截方法
2. 该项目使用的是`spring-web:5.3.8`版本,如有出入,请找对应的源码进行观看

#### 项目地址

项目测试地址为:https://github.com/fulln/logHelper

