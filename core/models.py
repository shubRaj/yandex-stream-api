from sqlalchemy import MetaData, Column, create_engine, Table, Integer,String,DateTime
from datetime import datetime
class DataAccessLayer:
    engine = None
    connection = None
    conn_string = None
    metadata = MetaData()
    yandex = Table("yandex", metadata,
        Column("id", Integer(), primary_key=True),
        Column("yandex_key",String(12),index=True,unique=True),
        Column("yandex_download_url",String(283),unique=True),
        Column("created",DateTime(),default=datetime.now),
        Column("updated",DateTime(),default=datetime.now,onupdate=datetime.now)
    )
    def db_init(self,conn_string):
        self.conn_string = conn_string
        self.engine = create_engine(conn_string)
        self.metadata.create_all(self.engine)
        # self.connection = self.engine.connect()
dal = DataAccessLayer()