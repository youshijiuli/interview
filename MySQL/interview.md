知呱呱（一家做专利申请业务平台的)

 上午10：30去面试的，去的太早了，早了2个多小时，第一次面试，也许是太激动，太紧张了。不过面的时候倒还好。
  先去前台填了表，然后等了一会，HR过来确认了一下信息，就把开发部的经理叫过来了。直接就在一个休息区面试了。

  1、先是让我做了一下自我介绍，很久没有做过自我介绍了，都快忘了我是谁，所以也就把自己的基本信息，毕业学校、专业，工作情况大致说了下。

  2、然后就看着简历上的信息，开始问了一下技术点

  a) MySQL的相关知识。
      存储引擎哪几种/有什么区别
      索引(有哪几种索引，索引之间的区别，索引的作用，什么情况下不适合建索引，组合索引的命中规则
      inner join/left join/right jion的区别

​    b) 项目相关：
​      rbac是个什么东西
​      rbac的实现逻辑，怎么做到限制到按钮级别的（忘记了，没回答好）
​      CMDB是做什么的（我写了这个项目，不过具体实现我并不知道，我回答的时候做了一下作用，具体实现说忘记了）

  c) python相关：
      classmethod和staticmethod的调用方式
      djang的请求流程



这份文件包含了多个面试题目，涵盖了数据库基础知识、SQL查询、数据插入、面向对象编程、函数式编程、以及数据处理等多个方面。下面是每个问题的简要描述和解答思路：

### 数据库基础知识
1. **smallint和int类型的区别**：`smallint`是2字节，`int`是4字节，它们能表示的数值范围不同。
2. **auto_increment-2631**：表示自增ID从2631开始。
3. **uniq_code, ix_province, ix_city**：这些是联合唯一索引，用于加速查找并确保数据唯一性。

### 数据查询
1. **查询2016年8月份每个station的平均值**：
   ```sql
   SELECT station, AVG(a), AVG(b), AVG(c) FROM history WHERE MONTH(time) = 8 AND YEAR(time) = 2016 GROUP BY station;
   ```
2. **查询2016年8月份每个station每天a不为空的记录数量**：
   ```sql
   SELECT s.code, s.province, s.city, COUNT(*) FROM history h JOIN stations s ON h.scode = s.code WHERE MONTH(h.time) = 8 AND YEAR(h.time) = 2016 AND h.a IS NOT NULL GROUP BY s.code, s.province, s.city;
   ```
3. **查询地区A和B两个站点2017年的a,b,c的平均值**：
   ```sql
   SELECT AVG(a), AVG(b), AVG(c) FROM history WHERE scode IN ('A', 'B') AND YEAR(time) = 2017;
   ```
4. **JOIN类型的区别**：
   - `INNER JOIN`：只连接匹配的行。
   - `LEFT JOIN`：左连接，显示左表的全部记录。
   - `RIGHT JOIN`：右连接，显示右表的全部记录。
   - `OUTER JOIN`：包含`LEFT JOIN`和`RIGHT JOIN`。

### 数据插入
1. **插入数据到history表**：
   ```sql
   INSERT INTO history (scode, time, a, b, c) VALUES ('CC1234', '2016-08-01', 11, 12, 11.12), ('CC1234', '2016-08-02', 11, 12, 11.12);
   ```
2. **从history_another表迁移数据到history表**：
   ```sql
   CREATE TABLE history_another LIKE history;
   INSERT INTO history_another SELECT * FROM history;
   ```
3. **分析SQL语句是否会执行失败**：如果`history`表中已有数据，且`history_another`表的结构与`history`不完全一致，或者在插入过程中违反了约束（如主键、唯一索引等），则可能执行失败。

### 二、数据库

设计数据库表，关系如下：
- 教师、班级、学生、科室
- 科室与教师为一对多关系
- 教师与班级为多对多关系
- 班级与学生为一对多关系
- 科室中需体现层级关系

1. **写出各张表的逻辑字段**：根据上述关系，设计数据库表的字段。
2. **根据上述表关系，查询**：
   - 教师id=1的学生数
   - 科室id=3的下级部门数
   - 所带学生最多的教师id

### 二、数据库基础

1. **SQL查询语句**

   (1) 查询所有数学成绩好于英语成绩的学生的姓名：

   ```sql
   SELECT s.name FROM student s
   JOIN grade m ON s.name = m.student_name AND m.course_name = 'math'
   JOIN grade e ON s.name = e.student_name AND e.course_name = 'english'
   WHERE m.score > e.score;
   ```

   (2) 查询所有没有学习过 'Alice' 老师的课的学生的姓名：

   ```sql
   SELECT s.name FROM student s
   WHERE s.name NOT IN (
       SELECT DISTINCT g.student_name FROM grade g
       JOIN course c ON g.course_name = c.name
       WHERE c.teacher_name = 'Alice'
   );
   ```

   (3) 查询各门课程的最高分和最低分：

   ```sql
   SELECT c.name AS course_name, MAX(g.score) AS max_score, MIN(g.score) AS min_score
   FROM course c
   JOIN grade g ON c.name = g.course_name
   GROUP BY c.name;
   ```

### 深蓝云海蓝沧科技软件设计开发人员考题（Python）

#### 一、必答题

#### 试题1. SQL查询语句填写

假设学生Students和教师Teachers关系模式如下所示：

- Students(学号，姓名，性别，类别，身份证号)
- Teachers(教师号, 姓名, 性别, 身份证号, 工资)

其中，学生关系中的类别分为“本科生”和“研究生”两类，性别分为“男”和“女”两类。

a. 查询研究生教师平均工资（显示为“平均工资”）、最高与最低工资之间差值（显示为“差值”）的SQL语句：

```sql
SELECT AVG(工资) AS 平均工资, MAX(工资) - MIN(工资) AS 差值
FROM Teachers
WHERE 类别 = '研究生';
```

b. 查询工资少于10000元的女研究生教师的身份证号和姓名的SQL语句（非嵌套查询方式）：

```sql
SELECT 身份证号, 姓名
FROM Teachers
WHERE 工资 < 10000 AND 性别 = '女' AND 类别 = '研究生';
```
