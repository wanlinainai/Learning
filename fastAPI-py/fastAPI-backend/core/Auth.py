from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.security import SecurityScopes
from fastapi import HTTPException, Request, Depends
from jwt import PyJWTError
from pydantic import ValidationError
from starlette import status

import jwt

from config import settings
from models.base import User

OAuth2 = OAuth2PasswordBearer(settings.SWAGGER_UI_OAUTH2_REDIRECT_URL, scheme_name="User",
                              scopes={"is_admin": "超级管理员", "not_admin": "普通管理员"})


def create_access_token(data: dict, issued_at: datetime = None):
    """
    创建Token
    :param data: Token数据
    :param issued_at: 签发时间，如果不传则使用当前时间
    :return: (jwt_token, issued_at) 返回Token和签发时间
    """
    token_data = data.copy()
    now = issued_at if issued_at else datetime.utcnow()
    expire = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({
        "exp": expire,
        "iat": now  # 添加签发时间
    })
    jwt_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_token, now


async def check_permission(req: Request, security_scopes: SecurityScopes, token=Depends(OAuth2)):
    """
    权限验证
    :param req:
    :param security_scopes:
    :param token:
    :return:
    """
    # ---------------------------------验证JWT Token-----------------------------------
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        if payload:
            # userID
            user_id = payload.get("user_id", None)
            user_type = payload.get("user_type", None)
            token_iat = payload.get("iat", None)  # 获取Token签发时间

            if user_id is None or user_type is None:
                credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="无效凭证",
                    headers={"WWW-Authenticate": f"Bearer{token}"}
                )
                raise credentials_exception

            # ---------------------------------验证Token是否已失效-----------------------------------
            # 查询用户最后登录时间
            user = await User.get_or_none(pk=user_id)
            if user and user.last_login_time and token_iat:
                # 将 token_iat (Unix时间戳) 转换为 datetime
                token_issued_at = datetime.utcfromtimestamp(token_iat)
                # 移除时区信息以便比较（统一为 timezone-naive）
                last_login = user.last_login_time.replace(tzinfo=None) if user.last_login_time.tzinfo else user.last_login_time

                # 添加2秒的容差时间，防止数据库精度问题
                # 只有当Token签发时间明显早于用户最后登录时间（超过2秒）时，才认为是旧Token
                time_tolerance = timedelta(seconds=2)
                if token_issued_at < (last_login - time_tolerance):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token已失效，请重新登录",
                        headers={"WWW-Authenticate": f"Bearer{token}"}
                    )
        else:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": f"Bearer{token}"}
            )
            raise credentials_exception

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已过期",
            headers={"WWW-Authenticate": f"Bearer{token}"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer{token}"}
        )
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer{token}"}
        )


    req.state.user_id = user_id
    req.state.user_type = user_type