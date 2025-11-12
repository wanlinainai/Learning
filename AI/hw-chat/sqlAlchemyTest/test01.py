from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, String, Double, Numeric, BOOLEAN, DateTime, create_engine, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# 创建对象的基类
Base = declarative_base()

class Test(Base):
    __tablename__ = 'test'

    # 表的结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=True)
    weight = Column(Double, nullable=True)
    money = Column(Numeric(9, 2), nullable=True)
    pet = Column(BOOLEAN, nullable=True)
    birthday_date = Column(DateTime, nullable=True)

    def __repr__(self):
        return f'<Test(id={self.id}, name={self.name}, weight={self.weight}, money={self.money}, pet={self.pet}, birthday_date={self.birthday_date})>'


# 初始化数据库连接
engine = create_engine('mysql+mysqlconnector://root:Zhang123454321.@192.168.121.129:3306/test')

# 创建DBSession类型
DBSession = sessionmaker(bind=engine)


if __name__ == '__main__':
    session = DBSession()

    new_test = Test(name="林则徐", weight=70.5, money=Decimal('9999.99'), pet=True, birthday_date=datetime(1994, 1, 1))

    # 添加到session中
    session.add(new_test)

    session.commit()

    session.close()