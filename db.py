from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import datetime

database_name = "main"

pg_db = PostgresqlExtDatabase(database_name, user='postgres', password='fgt6oij12c', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = pg_db

class MPK(BaseModel):
    id = AutoField(primary_key = True)
    id_kks = IntegerField(null = True)
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
        table_name = "МПК"

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