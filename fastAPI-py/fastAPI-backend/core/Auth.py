from datetime import datetime, timedelta

import jwt

from config import settings


def create_access_token(data: dict):
    """
    创建Token
    :param data:
    :return:
    """
    token_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp": expire})
    jwt_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_token