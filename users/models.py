from django.db import models
from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)

    class Meta:
        permissions = (
            ('can_view_contact_info', u'查看联系方式'),
        )

    def __str__(self):
        return self.user.username
# # Create your models here.
#
# #每个model默认都有三个permission，即 add model, change model 和 delete model
# class Permission(models.Model):
#     class Meta:
#         #权限信息，这里定义的权限的名字，后面是描述信息，描述信息是在django admin中显示权限用的
#         permissions = (
#             ('views_slg_users_tem', '查看玩家管理'),
#         )


