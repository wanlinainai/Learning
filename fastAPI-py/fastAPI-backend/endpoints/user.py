"""
用户管理相关路由
"""
from typing import Optional, List

from fastapi import APIRouter, Security, Request
from fastapi.params import Query

from config import settings
from core.Auth import create_access_token, check_permission
from endpoints.common import write_access_log
from models.base import User, Role, AccessLog
from schemas import user
from core.Response import fail, success, res_antd
from core.Utils import en_pass, check_pass
from tortoise.queryset import F

from schemas.user import UpdateUserInfo

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


@router.delete("", summary="删除用户", dependencies=[Security(check_permission, scopes=["user_delete"])])
async def user_del(req: Request, user_id: int):
    """
    删除用户
    :param req:
    :param user_id:
    :return:
    """
    if req.state.user_id == user_id:
        return fail(msg="You son of beach, are you fucking kidding me?")
    delete_result = await User.filter(pk = user_id).delete()
    if not delete_result:
        return fail(msg=f"用户{user_id}删除失败!")
    return success(msg="删除成功!")


@router.put("", summary="更新用户信息", dependencies=[Security(check_permission, scopes=["user_update"])])
async def user_update(post: user.UpdateUser):
    """
    更新用户信息
    :return:
    """
    user_check = await User.get_or_none(pk = post.id)
    # 超级管理员或者不存在的用户
    if not user_check or user_check.pk == 1:
        return fail(msg="用户不存在或不能删除")
    if user_check.username != post.username:
        check_username = await User.get_or_none(username = post.username)
        if check_username:
            return fail(msg=f"用户名{post.username}已经存在!")

    # 新密码
    if post.password:
        post.password = en_pass(post.password)

    data = post.dict()
    if not post.password:
        data.pop("password")
    data.pop("id")
    await User.filter(pk = post.id).update(**data)
    return success(msg="更新用户信息成功")


@router.get("", summary="用户列表", response_model=user.UserListData, dependencies=[Security(check_permission, scopes=["user_query"])])
async def user_list(
        pageSize: int = 10,
        current: int = 1,
        username: str = Query(None),
        user_phone: str = Query(None),
        user_status: bool = Query(None),
        create_time: List[str] = Query(None)
):
    """
    获取所有管理员
    :param pageSize:
    :param current:
    :param username:
    :param user_phone:
    :param user_status:
    :param create_time:
    :return:
    """
    query = {}
    if username:
        query.setdefault('username__icontains', username)
    if user_phone:
        query.setdefault('user_phone', user_phone)
    if user_status:
        query.setdefault('user_status', user_status)
    if create_time:
        query.setdefault('create_time__range', create_time)

    user_data = User.annotate(key=F("id")).filter(**query).all()
    # 总数
    total = await user_data.count()
    # 查询
    data = await user_data.limit(pageSize).offset(pageSize * (current - 1)).order_by("-create_time") \
    .values("key", "id", "username", "user_type", "user_phone", "user_email",
        "user_status", "header_img", "sex", "remarks", "create_time", "update_time")

    return res_antd(data=data, total=total, code=True)


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

        # 先生成Token并获取签发时间
        jwt_data = {
            "user_id": get_user.pk,
            "user_type": get_user.user_type
        }
        jwt_token, issued_at = create_access_token(data=jwt_data)

        # 使用Token的签发时间更新用户最后登录时间（确保完全一致）
        get_user.last_login_time = issued_at
        await get_user.save()

        data = {"token": jwt_token, "expire_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60}
        await write_access_log(req, get_user.pk, "通过账密登录了系统")

        return success(msg="登录成功", data=data)
    return fail(msg="请至少选择一种方法登录")


@router.get("/info", summary="获取登录用户信息", response_model=user.CurrentUser, dependencies=[Security(check_permission)])
async def user_info(req: Request):
    """
    获取当前登录用户
    :param req:
    :return:
    """
    user_data = await User.get_or_none(pk=req.state.user_id)
    if not user_data:
        return fail(msg=f"用户id{req.state.user_id}不存在!")
    # 非超级管理员


@router.get("/access/log", dependencies=[Security(check_permission)], summary="用户访问记录")
async def access_log(req: Request):
    """
    查询当前用户访问记录
    :param req:
    :return:
    """
    log = await AccessLog().filter(user_id=req.state.user_id).limit(10).order_by("-create_time") \
        .values("create_time", "ip", "note", 'id')
    return success(data=log)


@router.put("/info", dependencies=[Security(check_permission)], summary="更新用户的基本信息")
async def update_user_info(req: Request, post: UpdateUserInfo):
    """
    修改个人信息
    :param req:
    :param post:
    :return:
    """
    await User.filter(id=req.state.user_id).update(**post.dict(exclude_none=True))
    return success(msg="更新成功")

