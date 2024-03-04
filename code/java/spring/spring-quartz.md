#java #spring #定时任务
## spring-quartz 使用

### 介绍

spring-quartz是spring开发的定时任务执行调度执行,市面上大部分的定时任务中间件底层实现都是由spring-quartz实现,

如 :

* [xxl-job](https://www.xuxueli.com/xxl-job/ )

* [elastic-job](https://github.com/apache/shardingsphere-elasticjob)

有时间可以深入了解下,

### 甜品级demo

1. 引入pom

```xml

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-quartz</artifactId>
        </dependency>
```



2. 需要执行的具体逻辑

```java
@Slf4j
public class SimpleTask extends QuartzJobBean {

    @Override
    protected void executeInternal(JobExecutionContext jobExecutionContext) throws JobExecutionException {

        log.info("simpleTask is running----------->{} ",new Date());
    }
}
```



3. 配置对应config

```java
@Configuration
public class quartzConfig {

    @Bean
    public JobDetail firstJob(){
        return JobBuilder
                .newJob(SimpleTask.class)
                .withIdentity("job01")
                .storeDurably()
                .build();
    }
  
    @Bean
    public Trigger triggerQuartz(){
        SimpleScheduleBuilder scheduleBuilder = SimpleScheduleBuilder.simpleSchedule()
                .withIntervalInSeconds(5)
                .repeatForever();

        return TriggerBuilder
                .newTrigger()
                .forJob(firstJob())
                .withIdentity("job01")
                .withSchedule(scheduleBuilder)
                .build();
    }
}
```



结合数据库 可实现分布式集群布置 参考 https://www.cnblogs.com/tqlin/p/11064519.html 

