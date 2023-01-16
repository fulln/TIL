#tech

## 领域驱动设计

> Domain Driven Design (DDD) 

### DDD简介

我们在谈论到架构设计的时候，可以简化为三个层面：系统架构、技术架构和业务架构，这三者从三个不同的视角来描述我们的系统。系统架构关注系统的架构分层，技术架构决定使用的技术栈和框架。而作为一个偏向业务开发的工程师，我们日常施展拳脚的平台离不开业务架构这一层面，它根据业务需求设计相应的业务模块及其关系，决定了业务系统是否有足够的灵活性来面对业务的发展。 领域驱动设计 就是用来做业务架构设计的一种思想方法。

### 为啥用DDD

DDD是真正解决业务架构的思想：

* 把业务设计和业务开发统一，产品同学和研发同学统一
  * 统一在domain层，DDD的精华在这一层
  * 业务专家角色，在互联网领域大部分是缺失的，实际上是谁更懂谁就专家
* 业务和技术解耦
    * 本质上，DDD是把技术从业务中剥离：让业务成为中心，技术成为附属品
      * 技术是为业务服务的
      * 业务是业务，技术是技术，不要搅在一起
      * domain层，是业务核心：不要把业务模型和规则逃逸、泄露到其他层
        以领域为核心的分层架构，技术手段通过倒置依赖进行隔离
    * 是面向业务的设计和编程，不是面向数据库的编程，也不是面向技术实现的编程
      
    * 客观上起到了控制软件复杂度的作用,避免业务逻辑的复杂度与技术实现的复杂度混淆在一起，因为他们的变化维度和关注点不同
      
    * 把业务逻辑集中到domain一层，使得产品和研发能有一个共同的代码交流场所
      
        * UL落地到这一层
        
        * 前提是代码的业务表达力
    
* 统一并一致的领域建模和代码实现
  * 分析模型和设计模型不再割裂
  * 降低了出现不一致的可能性
* 改变过去Service + 数据库技术驱动开发模式
  * 回归业务本质，代码有更强的业务表达能力
  * 沉淀出反映领域知识并聚焦于关键概念的模型
  * 激发研发同学热情，解放研发生产力，不再束手束脚，可以充分发挥面向对象的优势写业务代码
    * 面向对象思想在解决业务问题上是非常理想的不二选择
    

### 定义

我们对架构、代码或组织做出的每一个决定都会对业务和用户产生影响。为了最有效地设计、构建和发展软件系统，我们的定义需要对项目业务正面影响，这只有在我们与业务目标保持一致并支持用户当前和潜在的未来需求时才能实现。根据部门业务,我以会员项目作为DDD实践的入口点进行分析

#### 分解

会员领域这个定义本身很宽泛，那我们要怎么来描述它呢？通常人在没有经过专业的模块化思维训练的情况下，时间是我们描述一个业务的基本维度。而在会员场景下,有下列时间相关流程

![image-20210811151140731](member.png)

整体流程以客户消费的阶段作为划分,现在我们只要将会员域分解为子域 - 域的松散耦合部分。

出于以下几个关键原因，我们将一个大的域分解为子域：

- 减少认知负荷，这样我们就可以独立地推理领域的各个部分，
- 给予开发团队自主权，以便他们可以处理解决方案的不同部分，
- 识别领域中的松耦合和高内聚，这会延续到我们的软件架构和团队结构。

根据这个思路,将会员领域分为了`会员运营` 和`会员权益`2个大部分对应流程图中前后2个状态

**以会员权益为例**

划分完大的方向后,我们需要更近一步,对领域内部进行更细粒度的划分:

![image-20210811154708850](submember.png)

不仅必须将大域分解为多个部分，而且还必须仔细设计这些部分之间的交互，以最大限度地减少不必要的耦合和复杂性。

#### 制定战略

战略性地规划子域：域中最有可能实现业务差异化或战略意义的部分。我们需要将重点集中在这个战略之上

#### 有界上下文定义

  会员权益子域整体结构图可以用下面一张图来表示

![img](ddd.jpeg)

* 名称
     会员权益子域

* 领域内容
  * 核心领域: 会员的档案,行为数据,身份信息,查询服务,
  * 支持领域:  发放基础权益
  * 通用领域: 

* 业务模型
  
     不直接暴露内部的数据信息,保持数据一致性
  
  * 直接来源: 用户直接输入的模型源,这里是回掉的kafka消息
  * 业务模型的参与源: 用户也需要,但是不会直接输入,如权益信息,各个需要发放的权益内容
  
* 水平任务编排

  将入口资源,领域内业务决策,出口资源编排成一个个执行的单元,如下图展示

  ![road](road.jpeg)

  * 接口的步骤编排,可以组织成对应泳道图,显示步骤的流转和编排

      在会员基础权益的编排中,水平步骤编排演如下

    ![image-20210811163519193](/Users/fulln/Library/Application Support/typora-user-images/image-20210811163519193.png)

### 工程实践

  > https://github.com/funkygao/cp-ddd-framework

在github搜索相关内容的时候,发现了一个针对DDD进行了代码设计的框架,下面是相关结构图

  ![img](https://camo.githubusercontent.com/81bd20f160c6cb3f2208a111e714665706a9c8cb069eb6f803d278d31f03fae8/687474703a2f2f7777772e706c616e74756d6c2e636f6d2f706c616e74756d6c2f7376672f584c4844526e436e344274784c756e7751572d666e334c514c497134663176304c5369544a556e397265684e5a6b705066415a716c70444537445746387441417678727679787474594a356f7470634c546a526c434d3837424e66705a3951504636704739486657674b4b4a5a6a506c632d50656b56726e566a5f543053555562414344306d5538546a696f36316a39696d7255674a7467374d753964626f5f6a48775176656b386152597a415032567a4b6e6e57766857795436475079695f646f6135547730756e4c5558472d695f6c7042763944394a453056306a5145665f4d696d7631774f4b5253545548525f634a3166512d59355150796b6737514f345a6d58327963464239347a48564d6b62307a4353444b365861576b6543636e686d304a56466b57496836746a5f6358505a4d794b336e4f4a484c30536232335f78303455594e54437274563344644654305978373733654c5a3641566d7045684d4b36386c3264485433794d596e63335074586975354b5564644153457a34486d424b794b5a554b31474f7275615a51655249516a42566748445666685f4748716d625f7555725448395370496d596b494d2d6632726e677649445a55635f393443527844733844696a6a4438464c51594e6c6a794a384c687a4234362d414d58717967476171735234536b585741466b737243336661744c774e415071775577464b55384641654568424b79336768696e4c4166724e716d7166596b44517767706774537442463746426456714a4261544e364d345a6942487a4e37516e4c484168625261343570476f4c5659426e5471626a6f4d6950506e724969636c4b44496475356175353235426579624e62537a5a593649746978734762326567796a52316132666e6f7443556b4457682d766772315f724f476559776653484847374c46746b486c5f637930)

  该框架除去Plugin部分,在使用过程中,将每个抽象的概念用代码具象化,通过代码弱约束,和校验框架的强约束(ArchUnit),来实现具体DDD模型,依据以上的开源项目对项目发放权益部分进行改造

在项目实践中,由于以轻量化代码为主,没全部引入开源框架,而是将领域代码分成了2个部分,

-  support类, 用来引入开源框架中的`IDomainService`,`IDomainModel`,`IDomainStep`等领域定义接口和脚手架代码
- service 类,这里面存放的是`step`,`domain`,`service`等业务相关的领域方面代码

而其他的`infrastructure,dependency `等划分没有使用,还是使用的传统的分层开发定义的结构,

实现功能聚焦的主要是会员基础权益发放,需要编排多个步骤,这里单个步骤整体的结构图形如下

  ![img](step.png) 

  整体权益发放流程图如下

  ![img](process.png)

​         在权益发放过程中, 调用基础权益领域时,将流转的过程隐藏,将业务具体流程和调用流程解耦

- step解耦合

  通过`stepCode`从spring容器中获取需要执行的步骤

  ```java
   		/**
       * 目前所有注册的step
       */
      private static Map<String, IDomainStep> stepMap;
  
      @SuppressWarnings("unchecked")
      public static <Step extends IDomainStep> List<Step> findSteps(List<String> stepCodes) {
          if (CollectionUtils.isEmpty(stepCodes)) {
              return Collections.emptyList();
          }
          return stepCodes.stream()
                  .distinct()
                  .map(stepCode -> (Step)stepMap.get(stepCode))
                  .filter(Objects::nonNull)
                  .collect(Collectors.toList());
      }
  ```

- step 执行

  ```java
  /**
       * 执行编排好的步骤，支持异步执行指定的步骤.
       * <p>
       * <p>步骤的实现里，可以通过{@link IReviseStepsException}来进行后续步骤修订，即动态的步骤编排</p>
       * <p>如果步骤实现了{@link IRevocableDomainStep}，在步骤抛出异常后会自动触发步骤回滚</p>
       * <p>异步执行的步骤，注意事项：</p>
       * <ul>
       * <li>需要使用者保证线程安全性!</li>
       * <li>beforeStep/afterStep的执行，都是同步的，都在主线程内执行</li>
       * <li>异步执行的步骤的异常都被忽略，不会触发回滚</li>
       * <li>不支持在异步执行的步骤里修订后续步骤</li>
       * </ul>
       * <p>In all, async steps executes in fire and forget mode!</p>
       *
       * @param stepCodes      待执行的的领域步骤
       * @param model          领域模型
       * @param taskExecutor   异步执行的线程池容器
       * @param asyncStepCodes 异步执行的步骤. Attention: 异步执行的任务，在失败时是不会触发回滚的
       * @throws FcboxMemberException 步骤执行时抛出的异常，统一封装为 FcboxMemberException
       */
      public final void execute(List<String> stepCodes, Model model,
                                SchedulingTaskExecutor taskExecutor, Set<String> asyncStepCodes) throws FcboxMemberException {
          if (stepCodes == null || stepCodes.isEmpty()) {
              log.warn("Empty steps on {}", model);
              return;
          }
  
          Stack<IRevocableDomainStep> executedSteps = new Stack<>();
          int stepRevisions = 0;
          while (++stepRevisions < MAX_STEP_REVISIONS) {
              // 执行步骤的过程中，可能会产生修订步骤逻辑
              stepCodes = executeSteps(stepCodes, executedSteps, model, taskExecutor, asyncStepCodes);
              if (stepCodes.isEmpty()) {
                  // 不再有步骤修订了：所有步骤都执行完毕
                  break;
              }
              // 修订了后续步骤，记录个日志，then next loop
              log.info("revised steps:{}", stepCodes);
          }
          if (stepRevisions == MAX_STEP_REVISIONS) {
              // e,g. (a -> b(revise) -> a)
              log.error("Steps revision seem to encounter dead loop, abort after {} model:{}", stepRevisions, model);
              throw FcboxMemberException.instance(ResultCodeEnum.SYS_EXCEPTION, "Seems steps dead loop, abort after " + MAX_STEP_REVISIONS);
          }
      }
  ```

  step的执行使用的开源项目中的`StepsExecTemplate`,在执行的过程中,可以中途加入或者减去对应的步骤,让整个流程会更加具有弹性

### 结语

对于某些项目可能只是将 DDD 应用于您的开发工作，对于其他项目,可能会跳过DDD,使用一些轻量级的传统分层方案。不要为了使用 DDD 而感到开发的不顺畅。 鉴于作者经验有限，对领域驱动设计的理解难免会有不足,欢迎大家共同探讨进步

### 参考

  1. https://virtualddd.com/learning-ddd
  2. https://github.com/ddd-crew/ddd-starter-modelling-process
  3. https://github.com/dddplus/dddplus
  4. https://tech.youzan.com/joker-ddd/

