import psycopg2
import os

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            port=os.environ['DB_PORT']
        )
        self.cursor = self.connection.cursor()

    def get(self,attr,tables,conditions=None):
        if conditions is not None:
            self.cursor.execute('SELECT ' + attr + ' FROM ' + tables + ' WHERE ' + conditions)
        else:
            self.cursor.execute('SELECT ' + attr + ' FROM ' + tables)
        return self.cursor.fetchall()

    def insert(self,table,attr,values):
        self.cursor.execute('INSERT INTO ' + table
            + ' (' + attr + ') VALUES (' + values + ')')
        self.connection.commit()

    def update(self,table,updates,conditions=None):
        if conditions is not None:
            self.cursor.execute('UPDATE ' + table
            + ' SET ' + updates + ' WHERE ' + conditions)
        else:
            self.cursor.execute('UPDATE ' + table
            + ' SET ' + updates)
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
