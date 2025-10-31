"""
Base database models
"""
from tortoise import fields, models


# 示例模型 - 可以根据需要添加更多模型
# class User(models.Model):
#     id = fields.IntField(pk=True)
#     username = fields.CharField(max_length=50, unique=True)
#     email = fields.CharField(max_length=100, unique=True)
#     created_at = fields.DatetimeField(auto_now_add=True)
#
#     class Meta:
#         table = "users"
