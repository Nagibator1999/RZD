from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import datetime
import pandas as pd

# замените на ваши значения
database_name = "main"
user = "postgres"
password = "fgt6oij12c"
host = "localhost"
port = 5432

pg_db = PostgresqlExtDatabase(database_name, user=user, password=password, host=host, port=port)

class BaseModel(Model):
    class Meta:
        database = pg_db

# след. три таблицы для листов из Сигналы.xlsx 
class MPK(BaseModel):
    id = AutoField(primary_key = True)
    id_kks = IntegerField(null = True)
    KKS = CharField(null = True)
    Суффикс = CharField(null = True)
    Модуль = CharField(null = True)
    Слот = IntegerField(null = True)
    Канал = IntegerField(null = True)
    NAME = CharField(null = True)
    Xmin_ = FloatField(null = True)
    Xmax_ = FloatField(null = True)
    unit = CharField(null = True)
    LA = FloatField(null = True)
    LW = FloatField(null = True)
    HW = FloatField(null = True)
    HA = FloatField(null = True)
    Точность_лог = FloatField(null = True)
    Точность_вк = FloatField(null = True)
    Type = CharField(null = True)

    class Meta:
        table_name = "МПК"

class RS485(BaseModel):
    id = AutoField(primary_key = True)
    kks = CharField(null = True)
    Суффикс = CharField(null = True)
    Модуль = CharField(null = True)
    Слот = IntegerField(null = True)
    Канал = IntegerField(null = True)
    name = CharField(null = True)
    xmin_ = FloatField(null = True)
    xmax_ = FloatField(null = True)
    unit = CharField(null = True)
    la = FloatField(null = True)
    lw = FloatField(null = True)
    hw = FloatField(null = True)
    ha = FloatField(null = True)
    Точность_лог = FloatField(null = True)
    Точность_вк = FloatField(null = True)
    type = CharField(null = True)

    class Meta:
        table_name = "RS458"

class Calculated(BaseModel):
    id = AutoField(primary_key = True)
    kks = CharField(null = True)
    Суффикс = CharField(null = True)
    Модуль = CharField(null = True)
    Слот = IntegerField(null = True)
    Канал = IntegerField(null = True)
    name = CharField(null = True)
    xmin_ = FloatField(null = True)
    xmax_ = FloatField(null = True)
    unit = CharField(null = True)
    type = CharField(null = True)
    Formula = FloatField(null = True)
    la = FloatField(null = True)
    lw = FloatField(null = True)
    hw = FloatField(null = True)
    ha = FloatField(null = True)
    Точность_лог = FloatField(null = True)
    Точность_вк = FloatField(null = True)

    class Meta:
        table_name = "Calculated"

# класс для таблицы архива
class Archive(BaseModel):
    id = AutoField(primary_key = True)
    id_kks = IntegerField(null = True)
    value = FloatField(null = True)
    session_date = DateTimeField()
    session_id = IntegerField(null = True)
    cycle_id = IntegerField(null = True)
    tm_update = FloatField(null = True)

    class Meta:
        table_name = "Archive"

def create_tables():
    with pg_db:
        pg_db.create_tables([MPK])

# функция для инициализации таблицы
def init():
    # важная ремарочка: в PostgreSQL имена колонок xmin, xmax
    # являются зарезервированными и их нельзя использователь в таблице

    create_tables()

    # заполняем таблцу МПК
    df = pd.read_excel('Сигналы.xlsx', sheet_name='МПК')
    data = df.to_dict(orient = 'records')
    print(data[0])
    with pg_db.atomic():
        MPK.insert_many(data).execute()
    print("Success")

if __name__ == '__main__':
    init()