import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Database(object):
    def __init__(self, 
                host = "localhost", 
                database = "test",
                user = "postgres", 
                port = 5432, 
                password = "fgt6oij12c"):

        self.host = host
        self.database = database
        self.user = user
        self.port = port
        self.password = password
        self.connection = None
        self.cursor = None

    # пересмотреть зачем оно
    # ну рил по-моему можно и нужно без неё
    def connect(self):
        if (self.connection):
            print("Connection already open")
            return
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                port=self.port,
                password=self.password)

            print("Connection to PostgreSQL established successfully")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)


    # возможные значения для action: CREATE/DROP
    def create_or_drop_database(self, name_of_database, action):

        # очень крутая штука
        # params = config()
        # conn = psycopg2.connect(**params)

        try:
            self.connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port)
            self.cursor = self.connection.cursor()

            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # хз зачем это но без него не работает

            sql_create_database = "{0} DATABASE {1};".format(action, name_of_database)
            self.cursor.execute(sql_create_database)

            print("PostgreSQL database created/dropped successfully)")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")


    # тут всё тоже гладко
    def create_table(self, name_of_database, name_of_table, columns, data_type_and_constraints):
        try:
            self.connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = name_of_database)
            self.cursor = self.connection.cursor()

            query_create_table = "CREATE TABLE {} (\n".format(name_of_table)

            query_tail = ""
            for column, dataTS in zip(columns, data_type_and_constraints):
                query_tail += column + " " + dataTS + ",\n"
            query_create_table += query_tail[:-2] + "\n);"

            self.cursor.execute(query_create_table)
            self.connection.commit()

            print("PostgreSQL table {0} in database {1} created successfully)".format(name_of_table, name_of_database))

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")        

    def insert(self, table, array_of_columns, array_of_values, name_of_database):
        try:
            self.connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = name_of_database)
            self.cursor = self.connection.cursor()
                
            columns = str(array_of_columns).replace("[","(").replace("]",")").replace("'", "")
            sql_insert_query = "INSERT INTO " + table + " " + columns + " VALUES ("
            for i in range(len(array_of_columns)):
                sql_insert_query += "%s,"
            sql_insert_query = sql_insert_query[:-1] + ")"

            self.cursor.executemany(sql_insert_query, array_of_values)
            self.connection.commit()
            print(self.cursor.rowcount, "Record inserted successfully into {} table".format(table))

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")

    def select_n_first_rows(self, table, name_of_database, number_of_rows):
        try:
            self.connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = name_of_database)
            self.cursor = self.connection.cursor()
            
            select_query = "SELECT * FROM {}".format(table)

            result = list()
            self.cursor.execute(select_query)

            for i in range(number_of_rows):
                result.append(self.cursor.fetchone())
            
            print("Selectring rows from table {} finished successfully".format(table))

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")
        return result

    def select_columns(self, table, name_of_database, number_of_rows, columns):
        try:
            self.connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = name_of_database)
            self.cursor = self.connection.cursor()
            
            result = dict()

            if type(columns) == str:
                columns = list(columns)

            for column in columns:
                select_query = "SELECT {0} FROM {1}".format(column,table)
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

        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")
        return result

    # получаем имена колонок
    def get_columns_names(self, table, name_of_database):
        try:
            self.connection = psycopg2.connect(user = self.user, password = self.password, host = self.host, port = self.port, database = name_of_database)
            self.cursor = self.connection.cursor()
            
            col_names = []
            for elt in self.cursor.description:
                col_names.append(elt[0])

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connection to PostgreSQL", error)

        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed") 
        return col_names      
            
        
if __name__ == "__main__":
    columns = ["id", "model", "price"]
    descr = ["INTEGER", "VARCHAR (50)", "REAL"]

    a = Database()
    # a.connect()
    # a.create_or_drop_database("to_delete", "CREATE")
    # a.create_table(name_of_database="to_delete", name_of_table="table_with_phones", columns=columns, data_type_and_constraints=descr)
    # a.insert("table_with_phones", ["id", "model"], [(1, "Pixel"), (2, "iPhone")], "to_delete")

    # lupa = a.select_n_first_rows("table_with_phones", "to_delete", 3)
    pupa = a.select_columns("table_with_phones", "to_delete", 2, ["id", "price"])
    print(pupa)
