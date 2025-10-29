from sqlalchemy_db import mysql_db
from model import TestModel

def query_all_data():
    print("正在查询数据库中的所有数据...")
    try:
        results = mysql_db.session.query(TestModel).all()

        if not results:
            print("数据库中没有数据")
        else:
            print(f"\n找到 {len(results)} 条记录:\n")
            print("-" * 80)
            for row in results:
                print(f"ID: {row.id}")
                print(f"姓名: {row.name}")
                print(f"体重: {row.weight}")
                print(f"金额: {row.money}")
                print(f"是否养宠物: {row.pet}")
                print(f"生日: {row.birthday_date}")
                print("-" * 80)
    except Exception as e:
        print(f"查询出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    query_all_data()
