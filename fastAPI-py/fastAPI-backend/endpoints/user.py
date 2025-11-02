"""
用户管理相关路由
"""
from fastapi import APIRouter, Security
from models.base import User, Role
from schemas import user
from core.Response import fail, success
from core.Utils import en_pass

router = APIRouter(prefix="/user")

"""
用户添加
"""
@router.post("", summary="添加用户")
async def add_user(post: user.CreateUser):
    # 判断用户是否存在？
    get_user = await User.get_or_none(username = post.username)
    if get_user:
        return fail(msg=f"用户名{post.username}已经存在!")
    post.password = en_pass(post.password)
    # 创建用户
    create_user = await User.create(**post.dict())
    if not create_user:
        return fail(msg=f"用户{post.username}创建失败!")
    # 是否存在分配角色
    if post.roles:
        roles = await Role.filter(role_status = True, id__in = post.roles)
        await create_user.role.add(*roles)

    return success(msg=f"用户{post.username}创建成功!")