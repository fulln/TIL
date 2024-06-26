---
dg-publish: true
---

#DDD #极客时间 

## 课程地址

> [12｜代码实现（下）：怎样更加“面向对象”？](https://time.geekbang.org/column/article/619447)

## 课程内容

### 领域对象的封装和继承

所谓“封装”，指的是将一个模块的实现细节尽量隐藏在内部，只向外界暴露最小的可访问接口,目的是减小模块间的耦合，提高程序的可维护性。

这里说的模块是广义的，一个函数、一个类、一个包乃至整个应用系统，都可以看作模块，而我们之前领域建模中说的模块模式是狭义的，专门指领域模型里的领域对象所组成的包。

#### 减少领域对象的 Setter

1. 限制 getter 和 setter 的数量
2. 表示业务含义的接口代替简单的 setter 和 getter

我们可以只为那些可以修改的属性保留 setter，其他的只有 getter，成为只读属性。再为 domain类增加一个包含只读属性的构造器，以便创建对象。

#### 通过“表意接口”提高封装性

直接通过访问domain类判断是否为有效组织。这实际上又是重构中的一种坏味道，叫做特性依恋（Feature Envy),解决方法是将判断逻辑移动到 domain 类内部.

对“表意接口”的运用，往往可以避免“特性依恋”的坏味道，反之，发现和消除“特性依恋”，也会重构出“表意接口”。

#### 用继承消除重复

**不要仅仅为了复用而使用继承**。判断父类和子类的关系，在语义上，是否有分类关系，或者概念的普遍和特殊关系。只有符合这种关系的，才能采用继承，否则应该用“组合”来实现复用。

### 编程风格

具体的编程风格是多种多样的，每种都各有利弊。因此，不可能也没有必要强求一致。关键是理解背后的原理，作出取舍，然后在自己的开发团队中形成比较统一的风格。

1. 领域对象不访问数据库。
	 在领域对象中既不会显式，也不会隐式访问数据库，目的是使领域对象和数据库解耦，便于维护和测试 
		 
2. 领域服务只能读数据库
	 领域服务需要读数据库。而写库的功能通常可以由应用服务来做，从而减轻领域层的负担。

3. 应用服务可以读写数据库
     纯粹的（通过调用仓库）读写数据库并不包含领域知识,更新一个对象前，要把这个对象先从数据库中读出来；创建或修改对象后，要存回数据库，这些本身都没有领域逻辑。

4. 用 ID 表示对象之间的关联
	 对象之间的关联应该用对象导航的方式来实现

5. 领域对象有自己的领域服务
	 如果是偏面向对象风格，很多领域逻辑可以在领域对象内部完成，因此不一定需要领域服务。但对于偏过程式的风格，由于领域对象不能访问数据库，很多领域逻辑就要外化到领域服务中，因此多数领域对象都会有相应的领域服务。

6. 在以上前提下利用封装和继承
	 即使是偏过程式的风格，如果善于利用封装、合理利用继承，也能有效提高程序质量。一个技巧是识别特性依恋的坏味道，并重构到表意接口。












