## MySQL数据库相关
  
### MySQL练习题  
[MySQL练习题参考答案](http://www.cnblogs.com/wupeiqi/articles/5748496.html)  

### 内联，左外联，右外联，全连接，交叉连接 的区别  
典型多对多联表查询:  
```sql
select man_to_women.nid,man.name as mname, women.name as wname from man_to_women  
left join man on man_to_women.man_id = man.nid  
left join women on man_to_women.women_id = women.nid  
where man.name = 'alex'  
```
左联:显示左边表的所有数据,只显示右边表与左边表有关联的数据  

### 什么是视图？以及视图的使用场景有哪些？  
视图是一种虚拟的表，具有和物理表相同的功能  
只暴露部分字段给访问者，所以就建一个虚表，就是视图。  
查询的数据来源于不同的表，而查询者希望以统一的方式查询，这样也可以建立一个视图，把多个表查询结果联合起来，查询者只需要直接从视图中获取数据，不必考虑数据来源于不同表所带来的差异  

### 视图作用  
数据库视图隐藏了数据的复杂性。  
数据库视图有利于控制用户对表中某些列的访问。  
数据库视图使用户查询变得简单。  

### 说一下事务的特性？  
__原子性(Atomicity)__：事务中的全部操作在数据库中是不可分割的，要么全部完成，要么均不执行。  
__一致性(Consistency)__：几个并行执行的事务，其执行结果必须与按某一顺序串行执行的结果相一致。  
__隔离性(Isolation)__：事务的执行不受其他事务的干扰，事务执行的中间结果对其他事务必须是透明的。  
__持久性(Durability)__：对于任意已交事务，系统必须保证该事务对数据库的改变不被丢失，即使数据库出  

### 什么是存储过程  
[简述存储过程](https://www.ilwid.net/posts/3b0cd4ca.html#%E5%AD%98%E5%82%A8%E8%BF%87%E7%A8%8B)  

### 创建一个完整的存储过程示例  
```sql
delimiter $$  # 修改结束符为$$, 以免程序把begin...end之间的;作为结束符  
drop procedure if exitsts proc_p1 $$  # 如果已经存在proc_p1就先删除  
create procedure proc_p1(  
    in i1 int  # 需要一个int类型的参数  
)  
begin  # sql逻辑代码要放在begin...end之间  
    declare d1 int;  # 声明一个d1变量  
    declare d2 int default 3;  # 声明一个默认值为3的d2变量  
    set d1 = i1 + i2;  
    select *from man_to_women where nid > d1;  
end $$  
deliniter ;  # 修改结束附为默认的分号,以免影响其他语句  

  # 调用存储过程  
call proc_p1(2)  
```

### sql注入原理  
sql注入漏洞产生的原因最常见的就是字符串拼接SQL语句,这种漏洞可以利用注释语句绕过验证  
如 `select name from userinfo where name='alex' and password = '888'`  
用户如果在name字段输入 `alex' or 1=1 --f` 就可以成功绕过验证。  
要解决这个问题就不能在程序中拼接sql语句,例如使用pymysql的execute方法,这个方法会自动对用户输入的引号特殊字符做转义  

### 简单说一说drop、delete与truncate的区别  
delete和truncate只删除表的数据不删除表的结构  
速度,一般来说: drop> truncate >delete  
delete语句是del,这个操作会放到rollback segement中,事务提交之后才生效;  
如果有相应的trigger,执行的时候将被触发。  
truncate,drop是ddl, 操作立即生效,原数据不放到rollback segment中,不能回滚. 操作不触发trigger。  
使用场景:  
不再需要一张表的时候，用drop  
想删除部分数据行时候，用delete，并且带上where子句  
保留表而删除所有数据的时候用truncate  

### 数据库怎么优化查询效率？  
通常会在WHERE、JOIN ON和ORDER BY使用到字段上加上索引。  
避免查询时判断NULL，否则可能会导致全表扫描。  
避免使用OR来连接查询条件，否则可能导致全表扫描，可以改用UNION或UNION ALL。  
避免LIKE查询，否则可能导致全表扫描。  
不使用SELECT *，只查询必须的字段，避免加载无用数据。  
能用UNION ALL的时候就不用UNION，UNION过滤重复数据要耗费更多的cpu资源。  
避免Update全部字段，否则频繁调用会引起明显的性能消耗，同时带来大 量日志  

  总结如下：  
1、避免模糊查询，如OR、LIKE等，因为会导致全表扫描；  
2、在常用字段加索引，例如WHERE、JOIN ON和ORDER BY使用到字段上应该加索引  
3、尽量避免全局性的读写操作，例如SELECT * 、Update全部字段  

### 数据库优化方案？  
1.优化索引、SQL 语句、分析慢查询;  
2.设计表的时候严格根据数据库的设计范式来设计数据库;  
3.使用缓存，把经常访问到的数据而且不需要经常变化的 数据放在缓存中，能节约磁盘 IO;  
4.优化硬件;采用 SSD，使用磁盘队列技术 (RAID0,RAID1,RDID5)等;  
5.采用 MySQL 内部自带的表分区技术，把数据分层不同 的文件，能够提高磁盘的读取效率;  
6.垂直分表;把一些不经常读的数据放在一张表里，节约 磁盘 I/O;  
7.主从分离读写;采用主从复制把数据库的读操作和写入操作分离开来;  
8.分库分表分机器(数据量特别大)，主要的的原理就是数据路由;  
9.选择合适的表引擎，参数上的优化;  
10.进行架构级别的缓存，静态化和分布式;  
11.不采用全文索引;  
12.采用更快的存储方式，例如 NoSQL 存储经常访问的数  

### Mysql 几种锁的区别  
* 表级锁：开销小，加锁快；不会出现死锁；锁定粒度大，发生锁冲突的概率最高，并发度最低。  
* 行级锁：开销大，加锁慢；会出现死锁；锁定粒度最小，发生锁冲突的概率最低，并发度也最高。  
* 页面锁：开销和加锁时间界于表锁和行锁之间；会出现死锁；锁定粒度界于表锁和行锁之间，并发度一般。  

  三种锁各有各的特点，若仅从锁的角度来说，表级锁更适合于以查询为主，只有少量按索引条件更新数据的应用，如WEB应用；行级锁更适合于有大量按索引条件并发更新少量不同数据，同时又有并发查询的应用，如一些在线事务处理（OLTP）系统。  

### 参考资料  
[常见面试题整理--数据库篇](http://blog.csdn.net/weinierzui/article/details/71054964)
