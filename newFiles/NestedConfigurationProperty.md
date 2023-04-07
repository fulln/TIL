#java #annotation #spring #javabasic 
##  @NestedConfigurationProperty

/**
 * Indicates that a field in a {@link ConfigurationProperties @ConfigurationProperties}
 * object should be treated as if it were a nested type. This annotation has no bearing on
 * the actual binding processes, but it is used by the
 * {@code spring-boot-configuration-processor} as a hint that a field is not bound as a
 * single value. When this is specified, a nested group is created for the field and its
 * type is harvested.
 */
 
意思就是一个嵌套类型，使用它了之后就不是一个简单单值了，一般是比较复杂的类型。另外，使用了这个注解的类，代表是不在本文件中，而是在其他地方。

