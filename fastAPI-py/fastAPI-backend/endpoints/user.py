"""
用户管理相关路由
"""
from fastapi import APIRouter, Security, Request

from config import settings
from core.Auth import create_access_token
from endpoints.common import write_access_log
from models.base import User, Role
from schemas import user
from core.Response import fail, success
from core.Utils import en_pass, check_pass

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

@router.delete("", summary="删除用户")
async def user_del(req: Request, user_id: int):
    """
    删除用户
    :param req:
    :param user_id:
    :return:
    """
    # if req.state.user_id == user_id:
    #     return fail(msg="You son of beach, are you fucking kidding me?")
    delete_result = await User.filter(pk = user_id).delete()
    if not delete_result:
        return fail(msg=f"用户{user_id}删除失败!")
    return success(msg="删除成功!")


@router.post("/account/login", response_model=user.UserLogin, summary="用户登录")
async def account_login(req: Request, post: user.AccountLogin):
    """
    用户登录
    :param req:
    :param post:
    :return:
    """
    if post.username and post.password:
        # 账密登录
        get_user = await User.get_or_none(username = post.username)
        if not get_user:
            return fail(msg=f"用户{post.username}密码验证失败!")
        if not get_user.password:
            return fail(msg=f"用户{post.username}密码验证失败!")
        if not check_pass(post.password, get_user.password):
            return fail(msg=f"用户{post.username}密码验证失败!")
        if not get_user.user_status:
            return fail(msg=f"用户{post.username}密码验证失败!")
        jwt_data = {
            "user_id": get_user.pk,
            "user_type": get_user.user_type
        }
        jwt_token = create_access_token(data=jwt_data)
        data = {"token": jwt_token, "expire_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60}
        await write_access_log(req, get_user.pk, "通过账密登录了系统")

        return success(msg="登录成功", data=data)
    return fail(msg="请至少选择一种方法登录")
