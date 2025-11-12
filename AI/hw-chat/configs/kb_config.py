
# 数据库连接信息
username='root'
hostname = "192.168.121.129"
database_name = "test"
password = "Zhang123454321."

SQLALCHEMY_DATABASE_URI = f'mysql+asyncmy://{username}:{password}@{hostname}/{database_name}?charset=utf8mb4'


KB_INFO = {
    "知识库名称": "知识库介绍",
    "samples": "关于本项目的ISSUES解答"
}