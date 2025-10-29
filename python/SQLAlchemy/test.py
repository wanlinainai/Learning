import datetime
import traceback

from sqlalchemy import func
from sqlalchemy_db import mysql_db
from model import TestModel

# 测试添加数据的方法
def test_add():
  print("开始测试添加数据...")

  test_obj = TestModel(
    name="张德彪",
    weight=120,
    money=88888.88,
    pet=False,
    birthday_date = datetime.datetime.now()
  )

  print(f"创建对象成功: {test_obj.name}")

  # 添加到数据库
  try:
    print("正在添加到数据库...")
    mysql_db.session.add(test_obj)

    # 提交数据
    print("正在提交事务...")
    mysql_db.session.commit()
    print(f"✓ 数据添加成功! ID: {test_obj.id}")

  except Exception as e:
    # 回滚数据
    print(f"✗ 发生错误，正在回滚...")
    mysql_db.session.rollback()
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("\n完整的错误堆栈:")
    traceback.print_exc()


# 批量添加数据
def test_add_batch():
  test_obj1 = TestModel(
    name = "张三丰",
    weight = 120,
    money = 10.00,
    pet = True,
    birthday_date = datetime.datetime.now()
  )

  test_obj2 = TestModel(
    name = "张三丰",
    weight = 120,
    money = 10.00,
    pet = True,
    birthday_date = datetime.datetime.now()
  )


  test_obj3 = TestModel(
    name = "张三丰",
    weight = 120,
    money = 10.00,
    pet = True,
    birthday_date = datetime.datetime.now()
  )

  mysql_db.session.add_all([test_obj1, test_obj2, test_obj3])

  # 提交数据
  mysql_db.session.commit()

# 测试修改数据，没有类似于Mybatis的update方法
def test_update():
  need_model = mysql_db.session.query(TestModel).filter(TestModel.id == 5).first()
  if need_model:
    need_model.name = "李太白"
    need_model.weight = 200
    need_model.money = 1.03

    # 提交数据
    mysql_db.session.commit()

    # 批量更新
    # mysql_db.session.query(TestModel).filter(TestModel.name == "张三丰").update({
    #   TestModel.name: '李太黑'
    # }, synchronize_session=False)
    # mysql_db.session.commit()

# 测试删除数据
def test_delete():
  # 此处的删除执行的是delete，不是逻辑删除
  delete_obj = mysql_db.session.query(TestModel).filter(TestModel.name == "张三丰").first()
  if delete_obj:
    mysql_db.session.delete(delete_obj)
    mysql_db.session.commit()

# 批量删除数据
def test_delete_batch():
  mysql_db.session.query(TestModel).filter(TestModel.name == '张三丰').delete(synchronize_session=False)

  mysql_db.session.commit()



# 查询
def test_query():

  # 如果query中是对应的模型，那么最终的查询出来的是所有字段
  test_obj1 = mysql_db.session.query(TestModel).all()
  test_obj2 = mysql_db.session.query(TestModel).first()

  # 如果query中只有部分字段，那么查询出来的就是选中的 部分字段
  test_obj3 = mysql_db.session.query(TestModel.name, TestModel.money).all()

  # 聚合函数：需要导入func 模块
  test_obj4 = mysql_db.session.query(func.count(TestModel.id)).first()
  test_obj5 = mysql_db.session.query(func.max(TestModel.id)).all()

  print("查询结果1: {}".format(test_obj1))
  print("查询结果2: {}".format(test_obj2))
  print("查询结果3: {}".format(test_obj3))
  print("查询结果4: {}".format(test_obj4))
  print("查询结果5: {}".format(test_obj5))



# 分页查询
def test_page1():
    page_size = 5

    current_page = 1

    # 第一页分页查询
    test_page_obj1 = mysql_db.session.query(TestModel.name).filter().limit(page_size).offset((current_page - 1) * page_size).all()
    print("test_page_obj1 = {}".format(test_page_obj1))
    # 第二页分页查询
    current_page = 2
    test_page_obj2 = mysql_db.session.query(TestModel.name).filter().limit(page_size).offset((current_page - 1) * page_size).all()
    print("test_page_obj2 = {}".format(test_page_obj2))

# 排序测试
def test_sort():
  # 升序
  test_obj1 = mysql_db.session.query(TestModel.id, TestModel.name).order_by(TestModel.id.asc()).all()
  print("升序: {}".format(test_obj1))

  # 降序
  test_obj2 = mysql_db.session.query(TestModel.id, TestModel.name).order_by(TestModel.id.desc()).all()
  print("降序: {}".format(test_obj2))



# 事务
def test_transaction():
  mysql_db.session.begin()
  try:
    test_model = TestModel(
      name = "事务",
      weight = 100,
      money = 1.00,
      pet = True,
      birthday_date = datetime.datetime.now()
    )

    # print(1 / 0)

    mysql_db.session.add(test_model)
    mysql_db.session.commit()
  except:
    mysql_db.session.rollback()
    raise

if __name__ == "__main__":
  print("="*50)
  print("测试脚本开始运行")
  print("="*50)
  # 测试添加数据
  # test_add()

  # 批量添加数据
  # test_add_batch()

  # 修改数据
  # test_update()

  # 删除数据
  # test_delete()

  # 批量删除数据
  # test_delete_batch()

  # 测试查询
  # test_query()

  # 分页查询
  # test_page1()

  # 排序测试
  # test_sort()

  # 测试事务
  test_transaction()


  print("="*50)
  print("测试脚本结束")
  print("="*50)