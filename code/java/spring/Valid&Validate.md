#java #spring #javabasic #valid #annotation

## @Valid 和 @Validate的区别

1. @Valid注解用于校验，所属包为：javax.validation.Valid。@Validated是@Valid 的一次封装，是Spring提供的校验机制使用。@Valid不提供分组功能
2. @Valid 和 @Validated 两者都可以对数据进行校验，待校验字段上打的规则注解（@NotNull, @NotEmpty等）都可以对 @Valid 和 @Validated 生效；
3. @Valid 进行校验的时候，需要用 BindingResult 来做一个校验结果接收。当校验不通过的时候，如果手动不 return ，则并不会阻止程序的执行；
4. @Validated 进行校验的时候，当校验不通过的时候，程序会抛出400异常，阻止方法中的代码执行，这时需要再写一个全局校验异常捕获处理类，然后返回校验提示。

