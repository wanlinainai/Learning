from typing import List

from fastapi import APIRouter, Query

from core.Response import fail, success, res_antd
from models.base import Role
from schemas.role import CreateRole, UpdateRole, RoleList
from tortoise.queryset import F

router = APIRouter(prefix="/role")


@router.post("", summary="添加角色")
async def create_role(post: CreateRole):
    """
    创建角色
    :param post:
    :return:
    """
    result = await Role.create(**post.dict())
    if not result:
        return fail(msg=f"角色创建失败!")
    return success(msg="角色创建成功")


@router.delete("", summary="删除角色")
async def delete_role(role_id: int):
    """
    删除角色
    :param role_id:
    :return:
    """
    role = await Role.get_or_none(pk = role_id)
    if not role:
        return fail(msg="角色不存在!")
    result = await Role.filter(pk = role_id).delete()
    if not result:
        return fail(msg="角色删除失败!")
    return success(msg="角色删除成功!")


@router.put("", summary="角色修改")
async def update_role(post: UpdateRole):
    """
    更新角色
    :param post:
    :return:
    """
    # 将id 删除
    param = post.dict()
    param.pop("id")
    result = await Role.filter(pk = post.id).update(**param)
    if not result:
        return fail(msg="角色更新失败!")
    return success(msg="角色更新成功!")


@router.get("", summary="角色列表")
async def get_all_role(
        pageSize: int = 10,
        current: int = 1,
        role_name: str = Query(None),
        role_status: bool = Query(None),
        create_time: List[str] = Query(None)
) -> RoleList:
    """
    角色列表
    :return:
    """
    query = {}
    if role_name:
        query.setdefault('role_name', role_name)
    if role_status is not None:
        query.setdefault('role_status', role_status)
    if create_time:
        query.setdefault('create_time__range', create_time)

    role = Role.annotate(key=F('id')).filter(**query).all()
    total = await role.count()
    data = await role.limit(pageSize).offset(pageSize * (current - 1)).order_by("-create_time") \
    .values("key", "id", "role_name", "role_status", "role_desc", "create_time", "update_time")

    return res_antd(code=True, data=data, total=total)