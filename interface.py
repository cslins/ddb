from database import *
import MySQLdb


class Interface:
    def __init__(self, clusters: list): #, conn: MySQLdb.Connection):
        self.clusters = clusters

        self.dataframes = {
        'Funcionário': {'columns-type': {'cpf': str, 'nome': str, 'num_dep': int},
        'partition_by': 'num_dep', 'partition_init': 1, 'partition_end': 5, 'partition_interval': round(5 / 3)},
        'Departamento': {'columns-type': {'num': int, 'nome': str},
         'partition_by': 'num_dep', 'partition_init': 1, 'partition_end': 5, 'partition_interval': round(5 / 3)}
        }

        self.replica_count = 1
        self.add_neighbors()
        self.query = ""

    def rcv_query(self, query):
        self.query = query

        return 


    def add_neighbors(self):
        for db in self.clusters:
            copy = self.clusters.copy()
            copy.remove(db)
            db.add_neighbor(copy)


    def add_data(self, table, query):
        pass

    def remove_data(self):
        pass

    def update_data(self):
        pass

    def select_data(self):
        pass

    def select_data_by_database(self, database: Database):
        pass













