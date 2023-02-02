
## 项目地址

http://jeecg.com

### 项目结构

#### git地址

- 前台: vue2
	- https://gitee.com/jeecg/ant-design-vue-jeecg
- 后台: jeecg-boot
	-  https://gitee.com/jeecg/jeecg-boot

## 主要功能实现

### 在线表单生成

在线菜单地址:
http://{localhost}:3000/online/cgform  --> Online表单开发

### 在线表单增强

1. 表单中选择按钮 _java增强_

### 动态表单接口

- 模型列表：
http://{localhost}:8080/jeecgboot/online/cgform/head/list?column=createTime&order=desc&pageNo=1&pageSize=10&copyType=0&_t=1672886625465

- 模型详情：
http://{localhost}:8080/jeecgboot/online/cgform/field/listByHeadId?headId=a0858db6dfcf4d8a9f49ead3f52c244a&_t=1672886708931

- 前端字段:
http://{localhost}:8080/jeecg-boot/online/cgform/api/getColumns/4028b28285fc0e9d0185fc0e9d900000?_t=1674971709
- 表单字段:
http://{localhost}:8080/jeecg-boot/online/cgform/api/getFormItem/4028b28285fc0e9d0185fc0e9d900000?_t=1674971709
- 查询条件:
http://{localhost}:8080/jeecg-boot/online/cgform/api/getQueryInfo/4028b28285fc0e9d0185fc0e9d900000?_t=1674971709
- 查询结果:
http://{localhost}:8080/jeecg-boot/online/cgform/api/getData/4028b28285fc0e9d0185fc0e9d900000?_t=1674971709&column=id&order=desc&pageNo=1&pageSize=10&superQueryMatchType=and
- 表单新增数据
http://{localhost}:8080/jeecg-boot/online/cgform/api/form/4028b28285fc0e9d0185fc0e9d900000?tabletype=1


####  1对多 代码生成部署

##### 创建
> ⚠️ 注意:生成的主键如果选择了分布式id, 则主键会采用`varchar`类型
1. 设置主表数据
2. 设置附表数据
3.  附表对应主表字段,外键设置主表名称和主表字段

##### 生成

生成url文档:http://doc.jeecg.com/2043916#b__38

- swagger配置需要手动修改对应包
- mapper 需要手动修改扫描包

##### 查询

1. 主表扩展配置打开联合查询
2. 子表对查询的字段勾选
3. 子表在展示的字段勾选

### 优化点:

1. 他表字段（多次关联后）回显异常，回显的是id，不是名称。影响列表和导出。
 >目前可以正常配置展示和导出.
2. 一张表按照不同条件生成不同视图：如员工表，生成在职员工视图、离职员工视图，即创建视图时支持选择筛选条件（或者写语句）。
> jeecg目前支持多视图
3.  树列表筛选数据无效，增加关联字段后列表错位
> http://10.204.210.26/online/cgformTreeList/997ee931515a4620bc30a9c1246429a9
4. 使用关联字段时候，关联表只能选列表内第一页
> 使用控件下拉搜索框 -> 填写对应表名 和字段映射