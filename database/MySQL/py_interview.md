##### MySQL如何创建索引
* ALTER TABLE
    * ALTER TABLE用来创建普通索引、UNIQUE索引或PRIMARY KEY索引。 
        * ALTER TABLE table_name ADD INDEX index_name (column_list)
        * ALTER TABLE table_name ADD UNIQUE (column_list)
        * ALTER TABLE table_name ADD PRIMARY KEY (column_list)
* CREATE INDEX
    * CREATE INDEX可对表增加普通索引或UNIQUE索引。
        *  CREATE INDEX index_name ON table_name (column_list)
        *  CREATE UNIQUE INDEX index_name ON table_name (column_list)

---

##### MySQL的增删改查
[参考链接](https://www.cnblogs.com/heyangblog/p/7624645.html)

* 增
    * 指定字段名
        * 语法：INSERT INTO 表名（字段名1，字段名2，…）VALUES（值1，值2，…）；
        * 举例：INSERT INTO student(id,name,grade) VALUES(1,'zhangshan',98);
    * 不指定字段名
        * 语法：INSERT INTO 表名 VALUES(值11，值2，…）；
        * 举例：INSERT INTO student VALUES (2,'lisi',62);
    * 其他写法
        * 语法：INSERT INTO 表名 SET 字段名1=值1[,字段名2=值2，…]
        * 举例：INSERT INTO student SET id=4，name='zhaoliu',grade=72;
    * 同时添加多条数据
        * 语法：INSERT INTO 表名[(字段名1，字段名2，…)] VALUES （值1，值2，…），（值1，值2，…），…（值1，值2，…）
        * 举例：INSERT INTO student VALUES (5，‘lilei’,99), (6,'hanmeimei',87), (8,'poly',76);
* 删
    * 删除部分数据
        * 语法：DELETE FROM 表名 [WHERE 条件表达式]
        * 命令：DELETE  FROM student WHERE id=7;
    * 删除全部数据
        * 语法：DELETE FROM 表名
        * 命令：DELETE FROM student；
    * 推荐的删除全部数据
        * 语法：TRUNCTE [TABLE ] 表名
        * 举例：TRUNCATE TABLE student
* 改
    * 更新部分数据
        * 语法：UPDATE 表名 SET 字段名1=值1，[ ，字段名2=值2，…] [ WHERE 条件表达式 ]
        * 命令：UPDATE student SET name=‘caocao’,grade=50 WHERE id=1;
    * 更新全部数据
        * 语法：UPDATE 表名 SET 字段名=值
        * 命令：UPDATE student SET grade=80；
* 查
    * 查询所有字段
        * 语法：SELECT 字段名1，字段名2，… FROM 表名 （该语法也可以查询部分字段）
        * 语法：SELECT * FROM 表名；
    * 按条件查询
        *  语法：SELECT 字段名1，字段名2，… FROM 表名 WHERE 条件表达式
        *  命令：SELECT id，name FROM student2  WHERE id=4;
    *  带IN关键字的查询
        *  语法：SELECT * | 字段名1，字段名2，… FROM 表名 WHERE 字段名 [ NOT ]  IN （元素1，元素2，…）
        *  命令：SELECT * FROM student2 WHERE id IN （1,2,3）；
    *  带 BETWEEN AND  关键字的查询
        *  语法：SELECT * | { 字段名1，字段名2，… } FROM  表名 WHERE 字段名 [ NOT ] BETWEEN  值1  AND  值2；
        *  命令：SELECT id,name FROM students WHERE id BETWEEN 2 AND 5;
    *  空值查询
        *  语法：SELECT * | 字段名1，字段名2，… FROM 表名 WHERE 字段名 IS [ NOT ] NULL
        *  命令：SELECT * FROM student2 WHERE gender IS NULL;
    *  带 DISTINCT 关键字的查询
        *  语法：SELECT DISTINCT 字段名 FROM 表名；
        *  命令：SELECT DISTINCT gender FROM student2;
    *  带 LIKE 关键字的查询
        *  语法：SELECT * | 字段名1，字段名2，… FROM 表名 WHERE 字段名 [ NOT ] LIKE ‘匹配字符串’;
        *  注意：%表示匹配任意长度的字符串，_表示匹配单个字符串
        *  命令：SELECT id,name FROM student2  WHERE name LIKE "S%"; 
        *  命令：SELECT id,name FROM student2 WHERE name LIKE 'w%g';
        *  命令：SELECT id,name FROM student2 WHERE name NOT LIKE '%y%';
        *  命令：SELECT * FROM student2 WHERE name LIKE 'wu_ong';
    *  带 AND 关键字的多条件查询
        *  语法：SELECT * | 字段名1，字段名2，… FROM 表名 WHERE 条件表达式1 AND 条件表达式2 [ … AND 条件表达式 n ];
        *  命令：SELECT id,name FROM student2 WHERE id<5 AND gender='女';
    *  带 OR 关键字的多条件查询
        *  语法：SELECT * | 字段名1，字段名2，… FROM 表名 WHERE 条件表达式1 OR 条件表达式2 [ … OR 条件表达式 n ];
        *  命令：SELECT id,name ,gender FROM student2 WHERE id<3 OR gender='女';
    *  AND和OR一起使用时，AND的优先级高于OR
    *  聚合函数
        *  COUNT()函数：统计记录的条数
            *  语法：SELECT COUNT(*) FROM 表名举例：
            *  命令：SELECT COUNT(*) FROM student2;
        *  SUM()函数：求出表中某个字段所有值的总和
            *  语法：SELECT  SUM(字段名) FROM 表名；
            *  命令：SELECT SUM(grade) FROM student2;
        *  AVG()函数：求出表中某个字段所有值的平均值
            *  语法：SELECT AVG(字段名) FROM 表名；
            *  命令：SELECT AVG(grade) FROM student2;
        *  MAX()函数：求出表中某个字段所有值的最大值
            *  语法：SELECT MAX(字段名) FROM 表名；
            *  命令：SELECT MAX(grade) FROM student2;
        *  MIN()函数：求出表中某个字段所有值的最小值
            *  语法：SELECT MIN(字段名) FROM 表名；
            *  命令：SELECT MIN(grade) FROM student2;
    *  对查询结果进行排序
        *  语法：SELECT 字段名1，字段名2，… FROM 表名 ORDER BY 字段名1 [ ASC | DESC ],字段名2 [ ASC | DESC ]
        *  (升序)命令：SELECT * FROM student2 ORDER BY grade;
        *  (降序)命令：命令：SELECT * FROM student2 ORDER BY grade DESC;
    *  分组查询
        *  语法：SELECT  字段名1，字段名2，… FROM 表名 GROUP BY 字段名1，字段名2，… [ HAVING 条件表达式 ];
        *  单独使用 GROUP BY 进行分组
            *  命令：SELECT * FROM student2 GROUP BY gender;
        *  GROUP BY 和聚合函数一起使用
            *  命令：SELECT COUNT(*) ,gender FROM student2 GROUP BY gender;
        *   GROUP BY 和 HAVING 关键字一起使用
            *   命令：SELECT sum(grade),gender FROM student2 GROUP BY gender HAVING SUM(grade) < 300;
    *   使用 LIMIT 限制查询结果的数量
        *   语法：SELECT 字段名2，字段名2，… FROM 表名 LIMIT [ OFFSET ,] 记录数
        *   (从0开始的4条)命令：SELECT * FROM student LIMIT 4;
        *   (从第五条开始的4条)命令：SELECT * FROM student2 ORDER BY grade DESC LIMIT 4,4;
    *   为表和字段取别名
        *   语法：SELECT * FROM 表名 [ AS ] 别名；
        *   命令：SELECT * FROM student2 AS s WHERE s.gender='女';
    *   为字段取别名
        *   语法：SELECT 字段名 [ AS ] 别名 [ ,字段名 [AS] 别名，…]  FROM 表名 ；
        *   命令：SELECT name AS stu_name,gender AS stu_gender FROM student2;

---

##### Mysql常见的函数
[参考链接](https://blog.csdn.net/qq646040754/article/details/82721801)

* ABS(x)：返回x的绝对值
* ROUND(x)：返回参数x的四舍五入的一个整数
* TRIM(str)：去除字符串两边的空白
* COUNT()：返回值的个数
* AVG()：返回平均值
* SUM()：求和

---

##### MySQL的建表语句
```mysql
#创建表，例子
#所谓的建表就是声明列的过程,所以要首先分析列
create table member(
    id int unsigned auto_increment primary key,
    username varchar(20) not null default '',
    gender char(1) not null default '',
    weight tinyint unsigned not null default 0,
    birth date not null default '0000-00-00',
    salary decimal(8,2) not null default 0.00,
    lastlogin int unsigned not null default 0
)engine myisam charset utf8;
```

---

##### Mysql常见数据库引擎及区别
[参考链接](https://www.cnblogs.com/yangjinwang/p/6433515.html)

* InnoDB：用于事务处理应用程序，具有众多特性，包括ACID事务支持。(提供行级锁)
* MyISAM：默认的MySQL插件式存储引擎，它是在Web、数据仓储和其他应用环境下最常使用的存储引擎之一。注意，通过更改STORAGE_ENGINE配置变量，能够方便地更改MySQL服务器的默认存储引擎。
* Memory：将所有数据保存再RAM中

---

##### mysql索引种类
[参考链接](https://blog.csdn.net/liutong123987/article/details/79384395)

* 普通索引：仅加速查询
* 唯一索引：加速查询 + 列值唯一（可以有null）
* 主键索引：加速查询 + 列值唯一（不可以有null）+ 表中只有一个
* 组合索引：多列值组成一个索引，专门用于组合搜索，其效率大于索引合并
* 全文索引：对文本的内容进行分词，进行搜索

---

##### 简述SQL注入原理，以及如何在代码层面房子sql注入

> 通俗点讲，SQL注入的根本原因是: "用户输入数据"意外变成了代码被执行。
> "用户输入数据"我这里可以指Web前端\$_POST,\$_GET获取的数据，也可以指从数据库获取的数据，当然也不排除程序猿无意中使用的特殊字符串。
> 在SQL语句的拼接中，一些含特殊字符的变量在拼接时破坏了SQL语句的结构，导致"用户输入数据"意外变成了代码被执行。

> 规避方法：
> 1. 理语句法  (解析协议层面上完全规避SQL注入)
> 2. 字符串转义（不要在sql中拼接字符）
> # query作为sql模板，args为将要传入的参数
> execute(query, args=None)

---

##### char和varchar的区别

1. 保存方式不一样
2. char有固定的长度，而varchar属于可变长的字符类型
3. char的效率比varchar高

---

##### 简述left join和right join的区别
* 左连接和右连接很相似，只是左右表位置的不同罢了。
* left join(左连接) 返回包括左表中的所有记录和右表中连接字段相等的记录 
* right join(右连接) 返回包括右表中的所有记录和左表中连接字段相等的记录

---

##### 为什么数据很大的时候使用limit offset分页时，越往后翻速度越慢，如何优化？
* 使用limit分页时，比如limit 10000，20的意思是扫描满足条件的10020行，扔掉前面的10000行，最后返回20行，问题就出在这，当数据量大的时候，大量时间花在了扫描上面了。
* 优化方法：
    * 当一个数据库表过于庞大，LIMIT offset, length中的offset值过大，则SQL查询语句会非常缓慢，你需增加order by，并且order by字段需要建立索引。
    * 如果使用子查询去优化LIMIT的话，则子查询必须是连续的，某种意义来讲，子查询不应该有where条件，where会过滤数据，使数据失去连续性

---

##### 使用python将数据库的student表中的数据写入db.txt
```python
import pymysql
connect=pymysql.Connect(
    host='',
    port=,
    user='',
    passwd='',
    db='',
    charset='',
)

cursor=connect.cursor()
sql='select * from student'
cursor.execute(sql)
students=cursor.fetchall()

with open('db.txt','w') as f:
    for student in students:
        f.write(student)
        
cursor.close()
connect.close()
```

---

##### 简述数据库分库分表
[参考链接](https://www.cnblogs.com/butterfly100/p/9034281.html)

* 垂直切分
    * 垂直分库：
        * 就是根据业务耦合性，将关联度低的不同表存储在不同的数据库
    * 垂直分表：
        * 基于数据库中的"列"进行，某个表字段较多，可以新建一张扩展表，将不经常用或字段长度较大的字段拆分出去到扩展表中。
* 横向切分：
    * 水平切分分为库内分表和分库分表，是根据表内数据内在的逻辑关系，将同一个表按不同的条件分散到多个数据库或多个表中，每个表中只包含一部分数据，从而使得单个表的数据量变小，达到分布式的效果。

---

##### MySQL的半同步复制原理
* 半同步复制，介于异步复制和全同步复制之间，主库在执行完客户端提交的事务后不是立刻返回给客户端，而是等待至少一个从库接收到并写到relay log中才返回给客户端。相对于异步复制，半同步复制牺牲了一定的性能，提高了数据的安全性。
* 异步复制，MySQL默认的复制是异步的，主库在执行完客户端提交的事务后会立即将结果返给给客户端，并不关心从库是否已经接收并处理。原理最简单，性能最好，但是主从之间数据不一致的概率很大。
* 全同步复制，指当主库执行完一个事务，所有的从库都执行了该事务才返回给客户端。因为需要等待所有从库执行完该事务才能返回，所以全同步复制的性能必然会收到严重的影响。

---

##### mysql慢日志
* MySQL的慢查询日志是MySQL提供的一种日志记录，它用来记录在MySQL中响应时间超过阀值的语句，具体指运行时间超过long_query_time值的SQL，则会被记录到慢查询日志中。

---

##### MySQL执行计划的作用和使用方法
[参考链接](https://blog.csdn.net/heng_yan/article/details/78324176)

* 作用：用来进行查询分析，比如整个查询涉及多少防，使用哪些索引，运行时间等
* 使用方法：使用explain关键字，如explain select xxx from xxx;

---

##### 数据库的导入与导出命令
* 导出(mysqldump)
    * 导出数据和表结构
        * mysqldump -uroot -p dbname > dbname .sql
    * 只导出表结构
        * mysqldump -uroot -p -d dbname > dbname .sql
* 导入
    * mysql -u用户名 -p密码 数据库名 < 数据库名.sql

---

##### 数据库锁的作用
[参考链接](https://blog.csdn.net/zhangzhetaojj/article/details/81559583)

* 锁分为三种：乐观锁，悲观锁和共享锁
* 数据库和操作系统一样，是一个多用户使用的共享资源。当多个用户并发地存取数据 时，在数据库中就会产生多个事务同时存取同一数据的情况。若对并发操作不加控制就可能会读取和存储不正确的数据，破坏数据库的一致性。加锁是实现数据库并 发控制的一个非常重要的技术。在实际应用中经常会遇到的与锁相关的异常情况，当两个事务需要一组有冲突的锁，而不能将事务继续下去的话，就会出现死锁，严 重影响应用的正常执行。

---

##### 列举创建索引但是无法命中索引的情况
[参考链接](http://www.cnblogs.com/zhuifeng-mayi/p/9285724.html)

1. 如果条件中有or，即使其中有条件带索引也不会使用(这也是为什么尽量少用or的原因）
2. 对于多列索引，不是使用的第一部分(第一个)，则不会使用索引
3. like查询是以%开头
4. 如果列类型是字符串，那一定要在条件中将数据使用引号引用起来,否则不使用索引
5. 如果mysql估计使用全表扫描要比使用索引快,则不使用索引

---

##### 索引再什么情况下遵循最左前缀的规则？
[参考链接](http://www.itdaan.com/blog/2018/07/09/65f5a78ed14d0e3374ba1ab8286a08af.html)

* 在多字段进行索引的时候，会遵循以上原则

---

##### 索引有什么作用，有哪些分类，有什么好处和坏处？
* 作用：为了增加查询速度，提高系统性能
* 分类：
    * 唯一索引：不允许其中任何两行具有相同索引值的索引。
    * 非唯一索引：允许其中任何两行具有相同索引值的索引。
    * 主键索引：有一列或列组合，其值唯一标识表中的每一行。
    * 聚集索引：表中行的物理顺序与键值的逻辑（索引）顺序相同。一个表只能包含一个聚集索引。  
* 好处：
    * 帮助用户提高查询速度 
    * 利用索引的唯一性来控制记录的唯一性 
    * 可以加速表与表之间的连接 
    * 降低查询中分组和排序的时间 
* 坏处：
    * 存储索引占用磁盘空间 
    * 执行数据修改操作(INSERT、UPDATE、DELETE)产生索引维护

---

##### 什么是索引合并

1. 索引合并是把几个索引的范围扫描合并成一个索引。
2. 索引合并的时候，会对索引进行并集，交集或者先交集再并集操作，以便合并成一个索引。
3. 这些需要合并的索引只能是一个表的。不能对多表进行索引合并。

---

##### 什么是覆盖索引

* 覆盖索引又可以称为索引覆盖。
    1. 解释一： 就是select的数据列只用从索引中就能够取得，不必从数据表中读取，换句话说查询列要被所使用的索引覆盖。　　
    2. 解释二： 索引是高效找到行的一个方法，当能通过检索索引就可以读取想要的数据，那就不需要再到数据表中读取行了。如果一个索引包含了（或覆盖了）满足查询语句中字段与条件的数据就叫做覆盖索引。　　
    3. 解释三： 是非聚集组合索引的一种形式，它包括在查询里的Select、Join和Where子句用到的所有列（即建立索引的字段正好是覆盖查询语句[select子句]与查询条件[Where子句]中所涉及的字段，也即，索引包含了查询正在查找的所有数据）。

---

##### 简述数据库的读写分离
[参考链接](https://www.cnblogs.com/0zcl/p/7141459.html)

* 读写分离就是在主服务器上修改，数据会同步到从服务器，从服务器只能提供读取数据，不能写入，实现备份的同时也实现了数据库性能的优化，以及提升了服务器安全。
