# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcntInfo(models.Model):
    aiid = models.AutoField(primary_key=True)
    aicharge = models.FloatField(blank=True, null=True)
    ailevel = models.CharField(max_length=6, blank=True, null=True)
    aibank = models.CharField(max_length=150, blank=True, null=True)
    aisubbranch = models.CharField(max_length=150, blank=True, null=True)
    aicardnumber = models.CharField(max_length=45, blank=True, null=True)
    ainame = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acnt_info'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Client(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=50)
    cbirthday = models.DateField(blank=True, null=True)
    csex = models.CharField(max_length=2)
    cposition = models.CharField(max_length=150, blank=True, null=True)
    clandline = models.CharField(max_length=50, blank=True, null=True)
    cmobile = models.CharField(max_length=50, blank=True, null=True)
    cemail = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'


class ClientCompany(models.Model):
    gid = models.AutoField(primary_key=True)
    gname = models.CharField(max_length=50)
    gtype = models.CharField(max_length=255, blank=True, null=True)
    gbclient = models.IntegerField()
    gpclient = models.IntegerField()
    ghalfhour = models.CharField(max_length=1, blank=True, null=True)
    gintroduction = models.TextField(blank=True, null=True)
    gremark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client_company'


class ClientOther(models.Model):
    gid = models.SmallIntegerField(primary_key=True)
    cid = models.SmallIntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client_other'
        unique_together = (('gid', 'cid'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ExpertChoosed(models.Model):
    piid = models.ForeignKey('ProjectInfo', models.DO_NOTHING, db_column='piid')
    eid = models.ForeignKey('ExpertInfo', models.DO_NOTHING, db_column='eid')
    state = models.CharField(max_length=2)
    itime = models.DateField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    starttime = models.DateTimeField(blank=True, null=True)
    endtime = models.DateTimeField(blank=True, null=True)
    totaltime = models.IntegerField(blank=True, null=True)
    notecreater = models.CharField(max_length=50, blank=True, null=True)
    epicharge = models.IntegerField(blank=True, null=True)
    ilhour = models.FloatField(blank=True, null=True)
    scorer = models.CharField(max_length=50, blank=True, null=True)
    s1 = models.IntegerField(blank=True, null=True)
    s2 = models.IntegerField(blank=True, null=True)
    s3 = models.IntegerField(blank=True, null=True)
    avgs = models.IntegerField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    aiid = models.IntegerField(blank=True, null=True)
    ecid = models.AutoField(primary_key=True)
    comment = models.IntegerField(blank=True, null=True)
    service = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expert_choosed'


class ExpertComments(models.Model):
    cmtid = models.AutoField(primary_key=True)
    eid = models.ForeignKey('ExpertInfo', models.DO_NOTHING, db_column='eid')
    eproblem = models.TextField(blank=True, null=True)
    ecomment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expert_comments'


class ExpertCommentsBackup(models.Model):
    cmtid = models.AutoField(primary_key=True)
    eid = models.ForeignKey('ExpertInfo', models.DO_NOTHING, db_column='eid')
    eproblem = models.TextField(blank=True, null=True)
    ecomment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expert_comments_backup'


class ExpertInfo(models.Model):
    eid = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=50)
    esex = models.CharField(max_length=2)
    emobile = models.CharField(max_length=50, blank=True, null=True)
    eemail = models.CharField(max_length=80, blank=True, null=True)
    etrade = models.CharField(max_length=150, blank=True, null=True)
    esubtrade = models.CharField(max_length=150, blank=True, null=True)
    ebirthday = models.DateField(blank=True, null=True)
    elandline = models.CharField(max_length=50, blank=True, null=True)
    elocation = models.CharField(max_length=150, blank=True, null=True)
    emsn = models.CharField(max_length=80, blank=True, null=True)
    eqq = models.CharField(max_length=50, blank=True, null=True)
    ephoto = models.CharField(max_length=20, blank=True, null=True)
    estate = models.IntegerField(blank=True, null=True)
    ecomefrom = models.TextField(blank=True, null=True)
    eremark = models.TextField(blank=True, null=True)
    admin_id = models.IntegerField(blank=True, null=True)
    addtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expert_info'


class ExpertInfoBackup(models.Model):
    eid = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=50)
    esex = models.CharField(max_length=2)
    emobile = models.CharField(max_length=50, blank=True, null=True)
    eemail = models.CharField(max_length=80, blank=True, null=True)
    etrade = models.CharField(max_length=150, blank=True, null=True)
    esubtrade = models.CharField(max_length=150, blank=True, null=True)
    ebirthday = models.DateField(blank=True, null=True)
    elandline = models.CharField(max_length=50, blank=True, null=True)
    elocation = models.CharField(max_length=150, blank=True, null=True)
    emsn = models.CharField(max_length=80, blank=True, null=True)
    eqq = models.CharField(max_length=50, blank=True, null=True)
    ephoto = models.CharField(max_length=20, blank=True, null=True)
    estate = models.IntegerField(blank=True, null=True)
    ecomefrom = models.TextField(blank=True, null=True)
    eremark = models.TextField(blank=True, null=True)
    admin_id = models.IntegerField(blank=True, null=True)
    addtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expert_info_backup'


class ExpertsExpertcomments(models.Model):
    cmtid = models.AutoField(primary_key=True)
    eproblem = models.TextField(blank=True, null=True)
    ecomment = models.TextField(blank=True, null=True)
    eid = models.ForeignKey('ExpertsExpertinfo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'experts_expertcomments'


class ExpertsExpertinfo(models.Model):
    eid = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=50)
    esex = models.CharField(max_length=2)
    emobile = models.CharField(max_length=50, blank=True, null=True)
    eemail = models.CharField(max_length=80, blank=True, null=True)
    etrade = models.CharField(max_length=150, blank=True, null=True)
    esubtrade = models.CharField(max_length=150, blank=True, null=True)
    ebirthday = models.DateField(blank=True, null=True)
    elandline = models.CharField(max_length=50, blank=True, null=True)
    elocation = models.CharField(max_length=150, blank=True, null=True)
    emsn = models.CharField(max_length=80, blank=True, null=True)
    eqq = models.CharField(max_length=50, blank=True, null=True)
    ephoto = models.CharField(max_length=20, blank=True, null=True)
    estate = models.IntegerField(blank=True, null=True)
    ecomefrom = models.TextField(blank=True, null=True)
    eremark = models.TextField(blank=True, null=True)
    admin_id = models.IntegerField(blank=True, null=True)
    addtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'experts_expertinfo'


class ExpertsWorkexp(models.Model):
    expid = models.AutoField(primary_key=True)
    stime = models.DateField(blank=True, null=True)
    etime = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    agency = models.CharField(max_length=150, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    duty = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    istonow = models.IntegerField(blank=True, null=True)
    eid = models.ForeignKey(ExpertsExpertinfo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'experts_workexp'


class MoneyCost(models.Model):
    eid = models.ForeignKey(ExpertInfo, models.DO_NOTHING, db_column='eid', primary_key=True)
    astandard = models.IntegerField(blank=True, null=True)
    alevel = models.CharField(max_length=6, blank=True, null=True)
    abank = models.CharField(max_length=150, blank=True, null=True)
    asubbranch = models.CharField(max_length=150, blank=True, null=True)
    acardnumber = models.CharField(max_length=35, blank=True, null=True)
    aname = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'money_cost'


class Mylog(models.Model):
    log = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mylog'


class OpLog(models.Model):
    user = models.CharField(max_length=50)
    optime = models.DateTimeField()
    opcode = models.IntegerField()
    main = models.IntegerField()
    sub = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'op_log'


class ProjectClient(models.Model):
    piid = models.ForeignKey('ProjectInfo', models.DO_NOTHING, db_column='piid', primary_key=True)
    gid = models.ForeignKey(ClientCompany, models.DO_NOTHING, db_column='gid')

    class Meta:
        managed = False
        db_table = 'project_client'


class ProjectDetail(models.Model):
    piid = models.ForeignKey('ProjectInfo', models.DO_NOTHING, db_column='piid', primary_key=True)
    eneed = models.IntegerField(blank=True, null=True)
    endtime = models.DateField(blank=True, null=True)
    comchannel = models.CharField(max_length=255, blank=True, null=True)
    isms = models.CharField(max_length=255, blank=True, null=True)
    dailyiquota = models.IntegerField(blank=True, null=True)
    pediscribe = models.TextField(blank=True, null=True)
    updatefreq = models.CharField(max_length=100, blank=True, null=True)
    premark = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_detail'


class ProjectInfo(models.Model):
    piid = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=150)
    pem = models.CharField(max_length=50)
    pemcontact = models.CharField(max_length=50, blank=True, null=True)
    pcode = models.CharField(max_length=50, blank=True, null=True)
    createtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'project_info'


class UsersMyuser(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'users_myuser'


class WorkExp(models.Model):
    expid = models.AutoField(primary_key=True)
    eid = models.ForeignKey(ExpertInfo, models.DO_NOTHING, db_column='eid')
    stime = models.DateField(blank=True, null=True)
    etime = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    agency = models.CharField(max_length=150, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    duty = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    istonow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_exp'


class WorkExpBackup(models.Model):
    expid = models.AutoField(primary_key=True)
    eid = models.IntegerField()
    stime = models.DateField(blank=True, null=True)
    etime = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    agency = models.CharField(max_length=150, blank=True, null=True)
    position = models.CharField(max_length=150, blank=True, null=True)
    duty = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)
    istonow = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'work_exp_backup'


class WorkerInfo(models.Model):
    wid = models.AutoField(primary_key=True)
    wname = models.CharField(max_length=50)
    waccount = models.CharField(max_length=50, blank=True, null=True)
    wpassword = models.CharField(max_length=50, blank=True, null=True)
    wrole = models.CharField(max_length=10)
    winfo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'worker_info'
