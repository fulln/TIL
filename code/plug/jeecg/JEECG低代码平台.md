
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
