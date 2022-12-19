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

    def add_data(self, replication_count, dict_op, replica=False):

        values_to_send = []
        if not replica:
            for value in dict_op['values']:
                if int(value[0]) % 3 == (int(self.name[-1]) - 1):
                    values_to_send.append(value)
        else:
            values_to_send = dict_op['values']

        print(values_to_send)

        query_distributed = f"""
        INSERT INTO {dict_op['table']} ({str(",".join([str(a) for a in dict_op['attributes']]))})
        VALUES {", ".join([f'({", ".join(at for at in v)})' for v in values_to_send])}
        """
        print(query_distributed)
        print(self.name)

        if len(values_to_send) > 0:
            self.cursor.execute(query_distributed)
            self.conn.commit()

        for v in values_to_send:
            dict_op['values'].remove(v)

        if len(dict_op['values']) > 0 and replica == False:
            self.neighbors[0].add_data(replication_count, dict_op)

        # comunicação
        if replication_count > 0 and replica == False:
            dict_op['values'] = values_to_send
            self.neighbors[0].add_data(replication_count - 1, dict_op, True)

    def remove_data(self, replication_count, table, condition=None, replica=False):

        if condition is None:

            query_distributed = f"""
            DELETE FROM {table}
            """
            self.cursor.execute(query_distributed)
            self.conn.commit()

            if not replica:
                self.neighbors[0].remove_data(0, table, replica=True)
                self.neighbors[1].remove_data(0, table, replica=True)

        else:
            query_distributed = f"""
            DELETE FROM {table}
            WHERE {condition['string']}
            """
            self.cursor.execute(query_distributed)
            self.conn.commit()

            if not replica:
                self.neighbors[0].remove_data(0, table, condition, replica=True)
                self.neighbors[1].remove_data(0, table, condition, replica=True)



    def update_data(self, replication_count, table, condition = None, replica=False):
        if condition['where'] is None:

            query_distributed = f"""
            UPDATE {table}
            SET {condition['set']}
            """
            self.cursor.execute(query_distributed)
            self.conn.commit()

            if not replica:
                self.neighbors[0].update_data(0, table, condition, replica=True)
                self.neighbors[1].update_data(0, table, condition, replica=True)

        else:
            query_distributed = f"""
            UPDATE {table}
            SET {condition['set']}
            WHERE {condition['where']}
            """
            self.cursor.execute(query_distributed)
            self.conn.commit()

            if not replica:
                self.neighbors[0].update_data(0, table, condition, replica=True)
                self.neighbors[1].update_data(0, table, condition, replica=True)

    def select_data(self, table: str, attributes: list, condition: dict = None, replica: bool = False):

        # list containing all results
        r = []

        # no where specified
        if condition is None:

            # produce query and execute
            query_distributed = f"""SELECT {attributes} FROM {table}"""
            print(query_distributed)
            self.cursor.execute(query_distributed)

            # check whether current data is replicated, fetch and replicate if necessary
            if not replica:
                r.append(self.cursor.fetchall())
                r.append(self.neighbors[0].select_data(table, attributes, replica=True))
                r.append(self.neighbors[1].select_data(table, attributes, replica=True))
        # there is a where
        else:
            # produce query and execute
            query_distributed = f"""
            SELECT {attributes} FROM {table}
            WHERE {condition['string']}
            """
            print(query_distributed)
            self.cursor.execute(query_distributed)

            # check whether current data is replicated, fetch and replicate if necessary
            if not replica:
                r.append(self.cursor.fetchall())
                r.append(self.neighbors[0].select_data(table, attributes, condition, True))
                r.append(self.neighbors[1].select_data(table, attributes, condition, True))

        # return results for a replica
        if replica:
            return self.cursor.fetchall()

        return r

    def get_data(self):

        self.cursor.execute("SELECT id, nome, cpf, n_departamento FROM funcionario")
        r1 = self.cursor.fetchall()

        self.cursor.execute("SELECT id, nome FROM departamento")
        r2 = self.cursor.fetchall()
        return r1, r2
