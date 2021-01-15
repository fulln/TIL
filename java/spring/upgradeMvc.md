## springMvc升级springBoot

	注意下使用的对应jar包的升级,其中升级mybatis的版本，造成新版本会检验强类型一致性，如果mybatis的xml的if test比较的类型相同的话，升级mybatis不会影响，否则需要把类型不一致进行比较要进行修改

### 升级步骤

####  Spring升级

1. 统一设置依赖管理

```java
<dependencyManagement>
        <dependencies>
            <dependency>
                <!-- Import dependency management from Spring Boot -->
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>2.4.1.RELEASE</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
</dependencyManagement>
```
2. 将项目中的对应的Spring相关的依赖替换成springboot相关

for example:web项目

```java
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

3. 更换项目打包插件
	* 修改当前pom中packageType为jar

		<packaging>jar</packaging>

	* 更换springboot打包插件
		```
		<plugin>
   			<groupId>org.springframework.boot</groupId>
   			<artifactId>spring-boot-maven-plugin</artifactId>
   			<executions>
      				<execution>
         				<goals>
            				<goal>repackage</goal>
         				</goals>
      				</execution>
   			</executions>
		</plugin>
		```
	* 增加springboot启动类与对应的配置文件application.yml,这里为了快速改造,建议将保留对应xml,使用`@ImportResource`的形式启动.
	
#### mybatis配置改造

springboot打包后的项目结构与war包相差很大,会导致mybatis找不到对应的实体

1. 升级mybatis

```xml
	<dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>${version.mybatis}</version>
        </dependency>
```
2. 新增VFS类

如果在项目中没有使用mybatis-start的包, 那就需要就加上这个类适配打包后的结构

```java
public class SpringBootVFS extends VFS {
 
    private final ResourcePatternResolver resourceResolver;
 
    public SpringBootVFS() {
        this.resourceResolver = new PathMatchingResourcePatternResolver(getClass().getClassLoader());
    
    }
 
    @Override
	    public boolean isValid() {
        return true;
    
	    }
 
    @Override
	    protected List<String> list(URL url, String path) throws IOException {
        Resource[] resources = resourceResolver.getResources("classpath*:" + path + "/**/*.class");
        List<String> resourcePaths = new ArrayList<String>();
	for (Resource resource : resources) {
            resourcePaths.add(preserveSubpackageName(resource.getURI(), path));
        
	}
        return resourcePaths;
    
	    }
 
    private static String preserveSubpackageName(final URI uri, final String rootPath) {
        final String uriStr = uri.toString();
        final int start = uriStr.indexOf(rootPath);
        return uriStr.substring(start);
    
    }

}
```

然后在sessionFactory中引入这个配置

```xml
<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
   <!-- 其他参数跟原来一样 -->
  <property name="vfs"  value="com.xxxx.SpringBootVFS"/>
</bean>
```

>  <b>注意</b> mybatis类型的校验问题,需要修改 非string类型的字段进行条件判断时,不能直接与''判空

#### web.xml修改为类加载模式

1. 如果是前后端未分离项目,需要增加webapp目录

```xml
<build>
   <resources>
      <resource>
        <directory>src/main/resources/</directory>
        <filtering>true</filtering>
      </resource>
      <resource>
        <directory>src/main/webapp</directory>
        <targetPath>static</targetPath> <!-- springboot读取html从/static目录下 -->
      </resource>
   </resources>
</build>
```
需要移动下对应前端文件的地址

2. application.yml 中需要配置对应view的地址

```yml
#JSP目录，不需要包括META-INF/resources目录
spring.mvc.view.prefix=/static/module/
spring.mvc.view.suffix=.jsp
```

3. 将web.xml 拦截器,过滤器,监听器 改成类加载模式

```java
@Configuration
public class CustomMvcConfiguration implements WebMvcConfigurer {
   //jdk的缓存监听器
    @Bean("introspectorCleanupListener")
    public ServletListenerRegistrationBean introspectorCleanupListener() {
        return new ServletListenerRegistrationBean<>(new IntrospectorCleanupListener());
    }

    @Bean
    public FilterRegistrationBean filterRegistrationEncoding() { //增加字符集的过滤器
        FilterRegistrationBean registrationBean = new FilterRegistrationBean();
        registrationBean.setFilter(characterEncodingFilter());
        registrationBean.addUrlPatterns("/*");
        registrationBean.setOrder(1);
        return registrationBean;
    }

    @Bean
    public CharacterEncodingFilter characterEncodingFilter() {
        CharacterEncodingFilter characterEncodingFilter = new CharacterEncodingFilter();
        characterEncodingFilter.setForceEncoding(true);
        characterEncodingFilter.setEncoding("UTF-8");
        return characterEncodingFilter;
    }

    //driud的拦截器
    @Bean
    @ConditionalOnMissingBean
    public StatViewServlet statViewServlet() {
        return new StatViewServlet();
    }

    @Bean("druidStatViewServletRegistration")
    public ServletRegistrationBean druidStatViewServletRegistration() {
        ServletRegistrationBean registration = new ServletRegistrationBean(
                statViewServlet(), "/druid/*");
        Map<String, String> map = new HashMap<>(1);
        map.put("resetEnable", "true");
        registration.setInitParameters(map);
        registration.setName("DruidStatView");
        return registration;
    }

```
4. 将mvc的xml 改成类加载形式

```java
	//国际化
    @Override
    protected void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        super.configureMessageConverters(converters);
        converters.add(new ByteArrayHttpMessageConverter());
        converters.add(new StringHttpMessageConverter(Charsets.toCharset("UTF-8")));
        converters.add(MappingJackson2HttpMessageConverter());
        converters.add(new BufferedImageHttpMessageConverter());
    }
	//文件上传
    @Bean
    public CommonsMultipartResolver multipartResolver() {
        return new CommonsMultipartResolver();
    }
    @Bean
    @ConditionalOnMissingBean
    public MappingJackson2HttpMessageConverter mappingJackson2HttpMessageConverter(){
        return new MappingJackson2HttpMessageConverter();
    }
 
    @Override
    protected void addInterceptors(InterceptorRegistry registry) {
        super.addInterceptors(registry);
         //增加App的拦截器
    }

```
#### 常见问题

1. log问题

建议使用springboot自带的对应log包

```
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-logging</artifactId>
</dependency>
```

2. 请求与返回乱码

去掉CharacterEncodingFilter的初始化，在application.properties里，增加下面配置
```
spring.http.encoding.force=true
spring.http.encoding.force-request=true
spring.http.encoding.force-response=true
```
3. 包冲突问题

这个就需要细致的排包工作

