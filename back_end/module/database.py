import mysql.connector as connector

class Condition:
    def __init__(self):
        self.data = {}

    def Append(self, column: str, value: str):
        self.data[column] = value

    def Create(self):
        clause = []
        
        for col in self.data.keys():
            clause.append(col + " = '%s'" % self.data[col])

        cdn = " AND ".join(clause)

        return cdn
        
class DbHandler:
    
    def __init__(
            self, 
            host: str, 
            port: int, 
            user: str, 
            password: str, 
            database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def Connect(self):   
        db = connector.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            database = self.database
        )

        return db
    
    def Insert(self, table: str, data: dict):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"

        self.ExecuteQuery_NoReturn(query, tuple(data.values()))

    def Update(self, table: str, data: dict, condition: str):
        clause = []
        for col in data.keys():
            clause.append(col + " = '%s'" % data[col])

        query = f"UPDATE {table} SET {','.join(clause)} WHERE {condition};"

        self.ExecuteQuery_NoReturn(query)

    def Select(self, table: str, colName: list):
        query = f"SELECT {', '.join(colName)} FROM {table};"
        return self.ExecuteQuery_Return(query)

    def SelectWhere(self, table: str, colName: list, condition: str):
        query = f"SELECT {', '.join(colName)} FROM {table} WHERE {condition};"
        return self.ExecuteQuery_Return(query)
    
    def ExecuteQuery_NoReturn(self, query: str, params=()):
        db = self.Connect()
        cursor = db.cursor() 

        try:
            cursor.execute(query, params) 
            db.commit() 

        except Exception as ex:
            raise ex

        finally:
            cursor.close() 
            db.close()  
        
    def ExecuteQuery_Return(self, query: str, params=()):
        db = self.Connect()
        cursor = db.cursor() 

        try:            
            cursor.execute(query, params) 
            data = cursor.fetchall()

        except Exception as ex:
            raise ex

        finally:
            cursor.close() 
            db.close() 

        return data



