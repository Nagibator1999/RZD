import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Database(object):
    def __init__(self, host = "127.0.0.1", database = "test", user = "postgres", port = 5432, password = "fgt6oij12c"):

        self.host = host
        self.database = database
        self.user = user
        self.port = port
        self.password = password
        self.connection = None
        self.cursor = None

    # подсоединяемся к базе данных
    # cur = True / создавать курсор или нет (по умолчанию - да)
    def connect(self, cur = True):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                port=self.port,
                password=self.password)
            if (cur):
                self.cursor = self.connection.cursor()

            print("Connection to PostgreSQL established successfully")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection is closed")


    # возможные значения для action: CREATE/DROP
    def create_or_drop_database(self, action):
        try:
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            sql_create_database = "{0} DATABASE {1};".format(action, self.database)
            self.cursor.execute(sql_create_database)

            print("PostgreSQL database created/dropped successfully)")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)


    def create_table(self, name_of_table, columns, data_type_and_constraints):
        try:
            query_create_table = "CREATE TABLE {} (\n".format(name_of_table)

            query_tail = ""
            for column, dataTS in zip(columns, data_type_and_constraints):
                query_tail += column + " " + dataTS + ",\n"
            query_create_table += query_tail[:-2] + "\n);"

            self.cursor.execute(query_create_table)
            self.connection.commit()

            print("PostgreSQL table {0} in database {1} created successfully)".format(name_of_table, self.database))

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)       

    def insert(self, table, columns, values):
        try:
            query = "INSERT INTO {0} {1} VALUES (".format(table, columns).replace("'","")
            query += ("%s,"*len(columns))[:-1]+")"
            values = tuple(values)

            self.cursor.executemany(query, values)
            self.connection.commit()
            print(self.cursor.rowcount, "Record inserted successfully into {} table".format(table))

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

    def update(self, table, rows, value_of_row, columns, values):
        try: 
            query = "Update {0} set {1} = %s where {2} = %s".format(table, columns, rows)

            # для архивации

            # если вдруг они окадутся неитерируемыми объектами
            values = tuple(values)
            value_of_row = tuple(value_of_row)

            records = list()

            for record, row in zip(values, value_of_row):
                tmp = [record, row]
                records.append(tuple(tmp))

            print(records)
            self.cursor.executemany(query, records)
            self.connection.commit()

            print("Records Updated")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

    def select_n_first_rows(self, table, number_of_rows):
        result = list()
        try:
            select_query = "SELECT * FROM {}".format(table)

            self.cursor.execute(select_query)

            for i in range(number_of_rows):
                result.append(self.cursor.fetchone())
            
            print("Selectring rows from table {} finished successfully".format(table))

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

        return result

    def select_columns(self, table, number_of_rows, columns, where = ""):
        result = dict()
        try:
            if type(columns) == str:
                columns = list(columns)

            for column in columns:
                select_query = "SELECT {0} FROM {1}".format(column,table)
                if (where != ""):
                    select_query += " where {}".format(where)
                self.cursor.execute(select_query)
                if number_of_rows == "ALL":
                    fatched = self.cursor.fetchall()
                    result[column] = fatched
                else:
                    fatched = self.cursor.fetchmany(number_of_rows)
                    result[column] = fatched
            
            print("Selectring columns from table {} finished successfully".format(table))

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

        return result

    # получаем имена колонок
    def get_columns_names(self, table):
        try:
            col_names = []
            for elt in self.cursor.description:
                col_names.append(elt[0])

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

        return col_names      
            
# сначала устанавливаем соединение (a.connect())
# потом делаем то нам нужно
# затем закрываем соединение (a.disconnect())

if __name__ == "__main__":
    columns = ["id", "model", "price"]
    descr = ["INTEGER", "VARCHAR (50)", "REAL"]

    a = Database(database="to_delete")
    a.connect()
    a.insert("table_with_phones", ("id", "model"), [(3, "Xiaomi"), (6, "Mezu")])
    
    # a.create_or_drop_database("to_delete", "CREATE")
    # a.create_table(name_of_database="to_delete", name_of_table="table_with_phones", columns=columns, data_type_and_constraints=descr)
    # a.insert("table_with_phones", ["id", "model"], [(1, "Pixel"), (2, "iPhone")], "to_delete")

    # lupa = a.select_n_first_rows("table_with_phones", "to_delete", 3)
    
    # pupa = a.select_columns("table_with_phones", 2, ["id", "price"], "id = 4")
    # print(pupa)

    # a.update("table_with_phones", "id", (1,2), "price", (30, 40))
    a.disconnect()

