from sqlalchemy import Boolean, Column, Date, Float, Integer, String, DECIMAL
from sqlalchemy.orm import declarative_base
from sqlalchemy_db import mysql_db



Base = declarative_base()

class TestModel(Base):
  __tablename__ = 'test'
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(20), nullable=True, comment="用户名")
  weight = Column(Float, comment="体重")
  money = Column(DECIMAL(9, 2), comment="钱数")
  pet = Column(Boolean, comment="是否养宠物")
  birthday_date = Column(Date, comment="出生日期")

Base.metadata.create_all(mysql_db.engine)