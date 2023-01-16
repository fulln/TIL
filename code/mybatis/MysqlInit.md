#mysql  #mybatis 

##   使用mybatis 自动执行脚本



### 执行步骤



- 添加包

  ```java
  <dependency>
     <groupId>org.mybatis.spring.boot</groupId>
     <artifactId>mybatis-spring-boot-starter</artifactId>
     <version>2.2.0</version>
  </dependency>
  <dependency>
     <groupId>mysql</groupId>
     <artifactId>mysql-connector-java</artifactId>
     <scope>runtime</scope>
  </dependency>
  ```

-  添加 sql执行脚本

  ​	脚本建议放在`resource`目录下面,方便查找和替换

- 添加脚本初始化类

  ```java
  @Slf4j
  @Component
  public class InitLockDataBase implements InitializingBean {
  
      @Autowired
      private DataSource dataSource;
  
      private static final String SQL_FILE_NAME = "init.sql";
  
      @Override
      public void afterPropertiesSet(){
          try {
              var scriptRunner = new ScriptRunner(dataSource.getConnection());
              var classPathResource = new ClassPathResource(SQL_FILE_NAME);
              var reader = new InputStreamReader(classPathResource.getInputStream());
              scriptRunner.runScript(reader);
          } catch (SQLException | IOException e) {
             log.info("[初始化sql脚本异常] 执行sql脚本异常,请检查",e);
               throw new IllegalStateException("sql脚本执行异常");
          }
      }
  }
  ```

- 启动项目

### 注意事项

1. 注意连接池的配置,spring默认版本是hikariCP的连接池,对应的application.yml中属性也要做修改
2. 注意sql脚本中sql后的`;` ,如果未检测到,则认为sql一直未执行完,将会报错.
3. 本项目使用了jdk15,如果启动不成功请切换对应的jdk版本.

### 项目地址

>  https://github.com/fulln/locks/releases/tag/scriptRunner

