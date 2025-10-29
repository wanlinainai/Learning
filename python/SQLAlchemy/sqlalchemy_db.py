from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import os
import dotenv

dotenv.load_dotenv()

class SQLAlchemy_db(object):
  def __init__(self):
    super(SQLAlchemy_db, self).__init__()

    self.engine = create_engine(
      url='mysql+pymysql://root:Zhang123454321.@192.168.121.129:3306/test',
      pool_size=10,
      max_overflow=10,
      pool_timeout=30,
      isolation_level="READ COMMITTED",
      pool_recycle=3600,
      pool_pre_ping=True
    )

    self.session = scoped_session(sessionmaker(bind=self.engine))

mysql_db = SQLAlchemy_db()