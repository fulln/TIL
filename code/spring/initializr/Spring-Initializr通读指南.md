---

---
## 文档解析

>文档地址： https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/

### 什么是 **Spring Initializr**

Spring Initializr 提供了一个可扩展的 API 来生成基于 JVM 的项目，并检查用于生成项目的元数据，例如列出可用的依赖项和版本。

您可以使用 Spring Initializr 轻松创建自己的实例，将 jar 用作您自己的应用程序中的库。涉及的代码最少，并且该服务具有非常丰富的配置结构，使您不仅可以定义各种项目属性的值，还可以定义依赖项列表以及应用于它们的约束。如果这听起来很有趣，那么[配置指南](https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/#configuration-guide)包含您需要的所有详细信息。您可能只想修改 Spring Initializr 的现有实例，例如添加新的依赖项类型，或更新现有依赖项类型的版本。对于这些以及其他简单和常见的用例，请查看 [“操作方法”指南](https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/#configuration-howto)。

Spring Initializr 还提供了一个可扩展的 API 来生成基于 JVM 的项目，并检查用于生成项目的元数据，例如列出可用的依赖项和版本。该 API 可以独立使用，也可以嵌入到其他工具中（例如，它用于 Spring Tool Suite、IntelliJ IDEA Ultimate、Netbeans 和 VSCode 等主要 IDE）。[API 指南](https://docs.spring.io/initializr/docs/current-SNAPSHOT/reference/html/#api-guide)中介绍了这些功能。

## 项目生成概述

Initializr 分为几个模块：

- `initializr-actuator`：可选模块，提供有关项目生成的附加信息和统计数据。    
- `initializr-bom`：提供物料清单，以便更轻松地管理项目中的依赖项。
- `initializr-docs`: 文档。
- `initializr-generator`：核心项目生成库。
- `initializr-generator-spring`：可选模块，定义典型 Spring Boot 项目的约定。可以重复使用或用您自己的约定替换。
- `initializr-generator-test`：项目生成的测试基础设施。
- `initializr-metadata`：项目各个方面的元数据基础设施。
- `initializr-service-sample`：展示一个基本的自定义实例。
- `initializr-version-resolver`：从任意 POM 中提取版本号的可选模块。
- `initializr-web`：第三方客户端的网络端点。

为了了解项目生成背后的概念，让我们 更详细地看`initializr-generator`一下。`initializr-generator-spring`

###  `initializr-generator`
该`initializr-generator`模块包含生成基于 JVM 的项目所需的低级基础设施。

#### Project Generator

类`ProjectGenerator`是项目生成的主要入口点。 `ProjectGenerator`定义`ProjectDescription`了要生成的特定项目以及`ProjectAssetGenerator`负责根据可用候选人生成资产的实现。

项目由`ProjectDescription`以下属性组成：

- 基本信息如`groupId`, `artifactId`, `name`,`description`
- `BuildSystem` 和 `Packaging`
- JVM`Language`
- 请求的依赖项，按 ID 索引
- `Version`项目使用的平台。这可用于根据所选代来调整可用的依赖项。
- `application` 名
- 根包名称
- 项目的基目录（如果与根目录不同）

项目生成发生在专用应用程序上下文 ( `ProjectGenerationContext`) 中，这意味着对于生成的每个项目，上下文仅包含与该特定项目相关的配置和组件。a 的候选组件`ProjectGenerationContext`在带注释的配置类中定义`@ProjectGenerationConfiguration`。如果在 中注册了这些配置类，则会自动导入这些配置类`META-INF/spring.factories`，如下例所示：

```
io.spring.initializr.generator.project.ProjectGenerationConfiguration=\
com.example.acme.build.BuildProjectGenerationConfiguration,\
com.example.acme.code.SourceCodeProjectGenerationConfiguration
```

添加到的组件`ProjectGenerationContext`通常具有可用的使用条件。使用条件可以避免暴露必须检查是否必须执行某些操作的 Bean，并使声明更加惯用。考虑以下示例：
```
@Bean
@ConditionalOnBuildSystem(GradleBuildSystem.ID)
@ConditionalOnPackaging(WarPackaging.ID)
public BuildCustomizer<GradleBuild> warPluginContributor() {
    return (build) -> build.plugins().add("war");
}
```

`BuildSystem`仅当要生成的项目使用“Gradle”和“war”时，这才会注册一个可以自定义 Gradle 构建的组件`Packaging`。查看 `io.spring.initializr.generator.condition`包以了解更多条件。您可以通过继承轻松创建自定义条件`ProjectGenerationCondition`。

您只能对已加载的 bean 使用此类条件， `ProjectGenerationConfiguration`因为它们需要具体的`ProjectDescription`bean 才能正常运行。

项目生成还可能依赖于不特定于特定项目配置的基础设施，并且通常在 main 中配置，`ApplicationContext`以避免每次新请求进入时都注册它。一个常见的用例是将 main 设置 `ApplicationContext`为`ProjectGenerationContext`,如下例所示：
```
public ProjectGenerator createProjectGenerator(ApplicationContext appContext) {
    return new ProjectGenerator((context) -> {
        context.setParent(appContext);
        context.registerBean(SampleContributor.class, SampleContributor::new);
    });
}
```
这将创建一个新的`ProjectGenerator`，可以使用应用程序的任何 bean，注册在`META-INF/spring.factories`中找到的所有contributors，并以编程方式注册一个额外的`ProjectContributor`。

项目生成还可能依赖于不特定于特定项目配置的基础设施，并且通常在主 ApplicationContext 中进行配置，以避免每次新请求进入时都进行注册。一个常见的用例是将主 ApplicationContext 设置为 ProjectGenerationContext，如以下示例所示：