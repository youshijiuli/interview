from django.db import models


# 联表查询用数据库分隔开
# Create your models here.
class member(models.Model):
    id_client = models.CharField(verbose_name="客户编号", max_length=16)
    name = models.CharField(verbose_name="姓名", max_length=50)
    email = models.CharField(verbose_name="联系方式", max_length=32, null=True, blank=True)


# models.member.create()

class provider(models.Model):
    provider_id = models.IntegerField(verbose_name="供应商编号")
    pro_name = models.CharField(verbose_name="供应商名称", max_length=50)
    linkman = models.CharField(verbose_name="联系人", max_length=50)
    linkWay = models.CharField(verbose_name="联系方式", max_length=50)
    city = models.CharField(verbose_name="城市", max_length=50)


class drugs(models.Model):
    drug_name = models.CharField(verbose_name="药品名称", max_length=50)
    # sup_id = models.IntegerField(verbose_name="供应商编号")
    # sup_id = models.ForeignKey(verbose_name="关联供应商", to="user", on_delete=models.CASCADE)
    product_id = models.CharField(verbose_name="生产批号", max_length=100)
    product_place = models.CharField(verbose_name="产地", max_length=50)
    type = models.CharField(verbose_name="所属类别", max_length=50)
    in_price = models.FloatField(verbose_name="进价", max_length=10)
    single_price = models.FloatField(verbose_name="单价", max_length=10)
    discount = models.FloatField(verbose_name="会员折扣", max_length=3)
    package = models.IntegerField(verbose_name="库存")
    size = models.CharField(verbose_name="规格", max_length=50)
    pro_date = models.DateField(verbose_name="生产日期")
    valid_date = models.DateField(verbose_name="有效期")


class user(models.Model):
    user_increment = models.CharField(verbose_name="用户编号", max_length=500)
    user_name = models.CharField(verbose_name="用户名", max_length=50)
    pwd = models.CharField(verbose_name="密码", max_length=50)
    type = models.CharField(verbose_name="类别", max_length=50)
    # balance = models.IntegerField(verbose_name="您的余额")


class manager(models.Model):
    manager_increment = models.CharField(verbose_name="经理编号", max_length=500)
    # user_increment = models.CharField(verbose_name="用户编号", max_length=500)
    user_increment = models.ForeignKey(verbose_name="关联用户编号", to="user", on_delete=models.CASCADE)


class worker(models.Model):
    worker_id = models.IntegerField(verbose_name="员工编号")
    worker_name = models.CharField(verbose_name="员工姓名", max_length=50)
    telephone = models.CharField(verbose_name="联系电话", max_length=500)
    # user_increment = models.CharField(verbose_name="用户编号", max_length=500)
    # 设置外码
    user_increment = models.ForeignKey(verbose_name="关联用户编号", to="user", on_delete=models.CASCADE)


class in_out(models.Model):
    io_number = models.IntegerField(verbose_name="收支编号")
    drug_id = models.IntegerField(verbose_name="药品")
    # worker_id = models.IntegerField(verbose_name="员工编号", max_length=500)
    # user_increment = models.ForeignKey(verbose_name="关联用户编号", to="user", on_delete=models.CASCADE, null=True,blank=True)
    user_increment = models.IntegerField(verbose_name="关联员工编号")
    number = models.IntegerField(verbose_name="数量")
    date = models.DateTimeField(verbose_name="日期")
    money = models.FloatField(verbose_name="总额", max_length=10)
    type = models.CharField(verbose_name="类别", max_length=50)


class in_document(models.Model):
    in_id = models.CharField(verbose_name="入库号", max_length=50)
    # provider_id = models.ForeignKey(verbose_name="管理供应商ID", to="provider", on_delete=models.CASCADE)
    # io_number = models.ForeignKey(verbose_name="关联收支编号", to="in_out", on_delete=models.CASCADE)
    provider_id = models.IntegerField(verbose_name="关联供应商ID")
    name = models.CharField(verbose_name="药品名称", max_length=50)
    io_number = models.IntegerField(verbose_name="关联收支编号")
    number = models.IntegerField(verbose_name="进货数量")


class sell_manage(models.Model):
    id_sell = models.IntegerField(verbose_name="销售编号")
    id_client = models.ForeignKey(verbose_name="关联客户编号", to="member", on_delete=models.CASCADE)
    io_number = models.ForeignKey(verbose_name="关联收支编号", to="in_out", on_delete=models.CASCADE)


class sales_returning(models.Model):
    id_returning = models.IntegerField(verbose_name="退货编号")
    id_sell = models.ForeignKey(verbose_name="关联销售编号", to="sell_manage", on_delete=models.CASCADE)
    io_number = models.ForeignKey(verbose_name="关联收支编号", to="in_out", on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name="退货数量")
