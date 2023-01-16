#mysql #json
## mysql的JSON字段类型

### 介绍

从 mysql 5.7.8 开始,MySQL 支持`JSON` 由[RFC 7159](https://tools.ietf.org/html/rfc7159)定义的本机数据类型 ，可以有效访问 JSON（JavaScript Object Notation）文档中的数据。该`JSON`数据类型与之前存储string相比,有以下几个优点：

* 校验存储的格式,非json格式的会存储报错
* 对json字段优化了存储结构,以便快速读取`json`的内部元素,当服务必须读取这种二进制json值时,不需要解析文本里面的内容

存储json文档所需要的空间与`Text`和`BLOB`相当,但是并不受到mysql单行最大值`65535`字节的限制,[`BLOB`](https://dev.mysql.com/doc/refman/5.7/en/blob.html)和 [`TEXT`](https://dev.mysql.com/doc/refman/5.7/en/blob.html),`json`列仅对行大小贡献 9 到 12 个字节，因为它们的内容与行的其余部分是分开存储。但是存储在`JSON`列中的任何 JSON 文档的大小都限于`max_allowed_packet`系统变量的值。

> [`max_allowed_packet`](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_max_allowed_packet)
>
> 一个数据包或任何生成/中间字符串或 API 函数发送的任何参数的最大大小 。默认值为 4MB。客户端最多可以接收与session值一样多的字节。但是，服务器无法向客户端发送比当前全局[`max_allowed_packet`](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_max_allowed_packet)值更多的字节 。（如果在客户端连接后更改了全局值，则全局值可能小于session值。）

`JSON`列与其他二进制类型的列一样，不直接索引；相反，可以在从列中提取标量值的生成列上创建索引 `JSON`。

```sql
mysql> CREATE TABLE jemp (
    ->     c JSON,
    ->     g INT GENERATED ALWAYS AS (c->"$.id"),
    ->     INDEX i (g)
    -> );
Query OK, 0 rows affected (0.28 sec)

mysql> INSERT INTO jemp (c) VALUES
     >   ('{"id": "1", "name": "Fred"}'), ('{"id": "2", "name": "Wilma"}'),
     >   ('{"id": "3", "name": "Barney"}'), ('{"id": "4", "name": "Betty"}');
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> SELECT c->>"$.name" AS name
     >     FROM jemp WHERE g > 2;
+--------+
| name   |
+--------+
| Barney |
| Betty  |
+--------+
2 rows in set (0.00 sec)

mysql> EXPLAIN SELECT c->>"$.name" AS name
     >    FROM jemp WHERE g > 2\G
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: jemp
   partitions: NULL
         type: range
possible_keys: i
          key: i
      key_len: 5
          ref: NULL
         rows: 2
     filtered: 100.00
        Extra: Using where
1 row in set, 1 warning (0.00 sec)
```

   

### mysql json相关函数

* [`JSON_ARRAY`](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array)json数组

  接受一个（可能是空的）值列表并返回一个包含这些值的 JSON 数组：

   ```sql
  mysql> SELECT JSON_ARRAY('a', 1, NOW());
  +----------------------------------------+
  | JSON_ARRAY('a', 1, NOW())              |
  +----------------------------------------+
  | ["a", 1, "2015-07-27 09:43:47.000000"] |
  +----------------------------------------+  
   ```

*  [`JSON_OBJECT`](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object) json对象

  接受一个（可能是空的）键值对列表并返回一个包含这些对的 JSON 对象：

  ```sql
  mysql> SELECT JSON_OBJECT('key1', 1, 'key2', 'abc');
  +---------------------------------------+
  | JSON_OBJECT('key1', 1, 'key2', 'abc') |
  +---------------------------------------+
  | {"key1": 1, "key2": "abc"}            |
  +---------------------------------------+
  ```

* [`JSON_QUOTE(`string`)`](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote) jsonString,通过用双引号字符包裹字符串并转义内部引号和其他字符，将`utf8mb4`字符串引用为 JSON 值，然后将结果作为字符串返回 。如果参数为`NULL`，则 返回 `NULL`。

  ```sql
  mysql> SELECT JSON_QUOTE('null'), JSON_QUOTE('"null"');
  +--------------------+----------------------+
  | JSON_QUOTE('null') | JSON_QUOTE('"null"') |
  +--------------------+----------------------+
  | "null"             | "\"null\""           |
  +--------------------+----------------------+
  mysql> SELECT JSON_QUOTE('[1, 2, 3]');
  +-------------------------+
  | JSON_QUOTE('[1, 2, 3]') |
  +-------------------------+
  | "[1, 2, 3]"             |
  +-------------------------+
  ```

* 搜索

  *  `$` 关键字,可以作为 JSON 表达式中字段的同义词。

    ```sql
    mysql> SELECT JSON_EXTRACT('{"id": 14, "name": "Aztalan"}', '$.name');
    +---------------------------------------------------------+
    | JSON_EXTRACT('{"id": 14, "name": "Aztalan"}', '$.name') |
    +---------------------------------------------------------+
    | "Aztalan"                                               |
    +---------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

    

  * 路径可以包含`*`或 `**`通配符：

    - `.[*]` 计算为 JSON 对象中所有成员的值。
    - `[*]` 计算 JSON 数组中所有元素的值。
    - Prefix *,*surfix 为所有以命名前缀开头并以命名后缀结尾的路径

    ```sql
    mysql> SELECT JSON_EXTRACT('{"a": 1, "b": 2, "c": [3, 4, 5]}', '$.*');
    +---------------------------------------------------------+
    | JSON_EXTRACT('{"a": 1, "b": 2, "c": [3, 4, 5]}', '$.*') |
    +---------------------------------------------------------+
    | [1, 2, [3, 4, 5]]                                       |
    +---------------------------------------------------------+
    mysql> SELECT JSON_EXTRACT('{"a": 1, "b": 2, "c": [3, 4, 5]}', '$.c[*]');
    +------------------------------------------------------------+
    | JSON_EXTRACT('{"a": 1, "b": 2, "c": [3, 4, 5]}', '$.c[*]') |
    +------------------------------------------------------------+
    | [3, 4, 5]                                                  |
    +------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

  * [`JSON_CONTAINS`](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains)

    通过返回 1 或 0 指示给定的 *`candidate`*JSON 文档是否包含在*`target`*JSON 文档中，或者如果提供了*`path`* 参数——是否在目标内的特定路径中找到了候选者。如果任何参数 `NULL`则返回 `NULL`，或者如果路径参数不识别目标文档的一部分。如果*`target`*或 *`candidate`*不是有效的 JSON 文档，或者*`path`*参数不是有效的路径表达式或包含 `*`或`**`通配符，则会发生错误 。

    如果仅检查路径中是否存在包含的数据，请用[`JSON_CONTAINS_PATH()`](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path)。

    以下为包含范围：

    - 当且仅当它们可比较且相等时，候选标量包含在目标标量中。两个标量值是可比的，如果他们有相同的 [`JSON_TYPE()`](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type)类型
    - 当且仅当候选中的每个元素都包含在目标的某个元素中时，候选数组才包含在目标数组中。
    - 当且仅当候选非数组包含在目标的某个元素中时，候选非数组才包含在目标数组中。
    - 当且仅当候选对象中的每个键在目标中都有一个同名的键，并且与候选键关联的值包含在与目标键关联的值中时，候选对象才包含在目标对象中。

    否则，候选值不包含在中。

    ```sql
    mysql> select count(*) from jemp where  json_contains(d,json_object('id','2'));
    +----------+
    | count(*) |
    +----------+
    |        1 |
    +----------+
    1 row in set (0.00 sec)
    ```

  * [`JSON_CONTAINS_PATH(`json_doc`, `one_or_all`, `path`[, `path`] ...)`](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path)

    判断某一路径是否存在

    ```sql
    mysql> select json_contains_path(d,'one','$[*].id') from jemp;
    +---------------------------------------+
    | json_contains_path(d,'one','$[*].id') |
    +---------------------------------------+
    |                                     1 |
    |                                  NULL |
    |                                  NULL |
    |                                  NULL |
    +---------------------------------------+
    ```

  * [`JSON_EXTRACT(`json_doc`, `path`[, `path`] ...)`](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract)

    从 JSON 文档中返回数据，从与*`path`* 参数匹配的文档部分中选择。返回`NULL`是否有任何参数是 `NULL`或没有路径在文档中定位值。如果*`json_doc`*参数不是有效的 JSON 文档或任何*`path`*参数不是有效的路径表达式，则会发生错误 。

    返回值由*`path`*参数匹配的所有值组成 。如果这些参数可能返回多个值，则匹配的值将自动包装为一个数组，顺序与生成它们的路径相对应。否则，返回值是单个匹配值。

    ```sql
    mysql> select  c, json_extract(d,'$[*].id') from jemp;
    +-------------------------------+---------------------------+
    | c                             | json_extract(d,'$[*].id') |
    +-------------------------------+---------------------------+
    | {"id": "1", "name": "Fred"}   | ["2", "2"]                |
    | {"id": "2", "name": "Wilma"}  | NULL                      |
    | {"id": "3", "name": "Barney"} | NULL                      |
    | {"id": "4", "name": "Betty"}  | NULL                      |
    +-------------------------------+---------------------------+
    4 rows in set (0.00 sec)
    ```

  * Column -> path

    ```sql
    mysql> select  c,c-> '$.name' from jemp;
    +-------------------------------+--------------+
    | c                             | c-> '$.name' |
    +-------------------------------+--------------+
    | {"id": "1", "name": "Fred"}   | "Fred"       |
    | {"id": "2", "name": "Wilma"}  | "Wilma"      |
    | {"id": "3", "name": "Barney"} | "Barney"     |
    | {"id": "4", "name": "Betty"}  | "Betty"      |
    +-------------------------------+--------------+
    ```

    数组

    ```
    mysql> select  d,d-> '$[*].name' from jemp;
    +--------------------------------------------------------------+--------------------+
    | d                                                            | d-> '$[*].name'    |
    +--------------------------------------------------------------+--------------------+
    | [{"id": "2", "name": "Wilma"}, {"id": "2", "name": "Wilma"}] | ["Wilma", "Wilma"] |
    | NULL                                                         | NULL               |
    | NULL                                                         | NULL               |
    | NULL                                                         | NULL               |
    +--------------------------------------------------------------+--------------------+
    4 rows in set (0.00 sec)
    ```

    

  * [`column`->>`path`](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path)

    不带引号的提取运算符

    ```sql
    mysql> select  c,c->> '$.name' from jemp;
    +-------------------------------+---------------+
    | c                             | c->> '$.name' |
    +-------------------------------+---------------+
    | {"id": "1", "name": "Fred"}   | Fred          |
    | {"id": "2", "name": "Wilma"}  | Wilma         |
    | {"id": "3", "name": "Barney"} | Barney        |
    | {"id": "4", "name": "Betty"}  | Betty         |
    +-------------------------------+---------------+
    4 rows in set (0.00 sec)
    ```

  * [`JSON_SEARCH`](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-search)

    可以用来判断是否存在

    ```
    mysql> select  json_search(d,'one','2') from jemp;
    +--------------------------+
    | json_search(d,'one','2') |
    +--------------------------+
    | "$[0].id"                |
    | NULL                     |
    | NULL                     |
    | NULL                     |
    +--------------------------+
    4 rows in set (0.00 sec)
    ```

    

* 比较

  JSON值可以使用进行比较 [`=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal)， [`<`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than)， [`<=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal)， [`>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than)， [`>=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal)， [`<>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal)， [`!=`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal)，和 [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to) 。

  JSON 值尚不支持以下比较运算符和函数：

  - [`BETWEEN`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between)
  - [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_in)
  - [`GREATEST()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_greatest)
  - [`LEAST()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_least)

  MySQL[`INT`](https://dev.mysql.com/doc/refman/5.7/en/integer-types.html)和 [`DOUBLE`](https://dev.mysql.com/doc/refman/5.7/en/floating-point-types.html)数字类型的两列之间的比较中,如果所有比较都涉及一个整数和一个double数,所有行的整数都转换为double数

 

