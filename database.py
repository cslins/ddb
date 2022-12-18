import pandas as pd
import MySQLdb
import credentials
import re

class Database:
    def __init__(self, name: str):
        self.name: str = name

        self.conn: MySQLdb.Connection = MySQLdb.connect(
            host=credentials.hostname,
            user=credentials.username,
            passwd=credentials.password,
            db=name
        )

        self.metadata: dict = {}
        self.neighbors: list = []
        self.cursor = self.conn.cursor()


    def add_neighbor(self, neighbors):
        for database in neighbors:
            self.neighbors.append(database)

        print('\nVizinhos de', self.name)
        for nb in self.neighbors:
            print(nb.name)

    def add_data(self, replication_count, query):
        query = """
INSERT INTO departamento (id, nome)
VALUES
    (1, "Memes"),
    (2, "Administrativo"),
    (3, "Financeiro"),
    (4, "Memes"),
    (5, "Administrativo"),
    (6, "Financeiro"),
    (7, "Memes"),
    (8, "Administrativo"),
    (9, "Financeiro"),
"""
        query_broken: list[str] = query.split("VALUES")  # ["INSERT INTO", "()\n()\n()"]

        insert_into = query_broken[0].split('(')
        table = insert_into[0][12:].strip()
        attributes = insert_into[1][:-2].split(',')

        values = query_broken[1].split("),")
        values_extracted = [v.strip()[1:].split(',') for v in values]
        values_needed = [v for v in values_extracted if len(v) == len(attributes)]
        values_clean = [i.replace('\"', '') for v in values_needed for i in v]

        dict_op = {
            "table": table,
            "attributes": attributes,
            "values": values_clean
        }

        for i in range(len(self.neighbors) + 1):
            self.neighbors[0]

        values_to_send = [1, '"Pesquisa"']

        query_distributed = f"""
        INSERT INTO {table} ({str(",".join([str(a) for a in attributes]))})
        VALUES ({str(",".join([str(v) for v in values_to_send]))})
        """
        print(query_distributed)
        self.cursor.execute(query_distributed)
        self.conn.commit()

        # comunicação
        if replication_count > 0:
            self.neighbors[0].add_data(replication_count - 1, query)

    def remove_data(self, replication_count, query):

        if replication_count > 0:
            self.neighbors[0].remove_data(replication_count - 1, query)

    def update_data(self, replication_count, table, data: dict, condition=None):
        pass

    def select_data(self, table, columns: list, condition=None):
        pass

    def get_data(self):

        self.cursor.execute("SELECT id, nome, cpf, n_departamento FROM funcionario")
        r1 = self.cursor.fetchall()

        self.cursor.execute("SELECT id, nome FROM departamento")
        r2 = self.cursor.fetchall()
        return r1, r2
