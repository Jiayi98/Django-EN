# Django-EN
### steps for updating on server
1.ps -ulianghaitao x
2.kill process
3.退出mysite
4.进入expert_network_master文件夹
5.rename mysite文件夹
6.upload 新代码
7.cd mysite
8.nohup uwsgi --http :1973 --module mysite.wsgi &>/home/expert_network_master/expert_network.txt &
### steps for modifying permissions
#### Group
1.修改该分组的权限
#### User
1.直接修改user所属的group
