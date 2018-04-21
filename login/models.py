from django.db import models

# Create your models here.

class User(models.Model):
    gender = (
        ('female', '女'),
        ('male', '男')
    )
    name = models.CharField(max_length=50, unique=True) # 用户名
    password = models.CharField(max_length=100) # 密码
    email = models.CharField(max_length=100) # 邮箱
    sex = models.CharField(max_length=20, choices=gender, default='男') # 性别
    c_time = models.DateTimeField(auto_now_add=True) # 添加时间

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

