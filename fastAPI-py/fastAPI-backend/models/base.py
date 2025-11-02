"""
Base database models
"""
from tortoise import fields, models, Model


class TimestampMixin(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True

class User(TimestampMixin):
    role: fields.ManyToManyRelation["Role"] = \
        fields.ManyToManyField("base.Role", related_name="user", on_delete=fields.CASCADE)
    username = fields.CharField(null=True, max_length=20, description="用户名")
    user_type = fields.BooleanField(default=False, description="用户类型：True:超级管理员，False:普通管理员")
    password = fields.CharField(null=True, max_length=255, description="用户密码")
    nickname = fields.CharField(default="BITCH_NIGGA", max_length=255, description="昵称")
    user_phone = fields.CharField(null=True, max_length=11, description="手机号")
    user_email = fields.CharField(null=True, description="邮箱", max_length=255)
    full_name = fields.CharField(null=True, description="姓名", max_length=255)
    user_status = fields.IntField(default=0, description="0 未激活；1 正常；2 禁用")
    header_img = fields.CharField(null=True, description="头像", max_length=500)
    sex = fields.IntField(default=0, description="0 未知；1 男；2 女")
    remarks = fields.CharField(null=True, description="备注", max_length=1024 * 10)
    client_host = fields.CharField(null=True, description="访问IP", max_length=50)
    last_login_time = fields.DatetimeField(null=True, description="最后登录时间")

    class Meta:
        table_description = "用户表"
        table = "user"


class Role(TimestampMixin):
    user: fields.ManyToManyRelation[User]
    role_name = fields.CharField(max_length=20, description="角色名称")
    role_status = fields.BooleanField(default=False, description="True：用户启用状态, False： 用户关闭状态")
    role_desc = fields.CharField(null=True, max_length=255, description="角色描述")
    class Meta:
        table_description = "角色表"
        table = "role"


class AccessLog(TimestampMixin):
    user_id = fields.IntField(description="用户id")
    target_url = fields.CharField(null=True, description="访问的URL", max_length=255)
    user_agent = fields.CharField(null=True, description="访问UA", max_length=255)
    request_params = fields.JSONField(null=True, description="请求参数get|post")
    ip = fields.CharField(null=True, max_length=32, description="访问IP")
    note = fields.CharField(null=True, max_length=255, description='备注')

    class Meta:
        table_description = "用户操作记录表"
        table = "access_log"