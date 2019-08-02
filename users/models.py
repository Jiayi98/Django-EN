from django.db import models
from django.conf import settings
# from django.contrib.auth.models import AbstractUser
# from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)

    class Meta:
        managed = True
        db_table = 'users_myuser'
        permissions = (
            ('can_view_expert_contact_info', u'查看专家联系方式'),
            ('can_change_expert_contact_info', u'修改专家联系方式'),
            ('can_delete_expert_workexp', u'删除专家工作经历'),
            ('can_delete_expert_comments', u'删除专家评论'),
            ('can_add_project_interview_1', u'新增项目访谈'),

            ('can_delete_project_interview', u'删除项目访谈'),
            ('can_change_project_interview', u'修改项目访谈'),
            ('can_view_project_interview', u'查看项目访谈'),
            ('can_change_all_project_interview', u'修改所有项目访谈'),
            ('can_view_all_project_interview', u'查看所有项目访谈'),

            ('can_add_client', u'新增客户'),
            ('can_view_client_info', u'查看客户信息'),
            ('can_change_client_info', u'修改客户信息'),
            ('can_delete_client_info', u'删除客户信息'),

            ('can_view_cfee', u'查看客户咨费'),
            ('can_change_cfee', u'修改客户咨费'),

            ('can_add_client_bc_fc', u'新增客户联系人'),
            ('can_view_client_bc_fc_contact', u'查看客户联系人联系方式'),
            ('can_change_client_bc_fc_contact', u'修改客户联系人联系方式'),
            ('can_delete_client_bc_fc_contact', u'删除客户联系人联系方式'),
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


