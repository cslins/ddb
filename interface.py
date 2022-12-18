from database import *

class Interface:
    def __init__(self, cluster: list):
        self.cluster = cluster

        self.dataframes = {
        'Funcionário': {'columns-type': {'cpf': str, 'nome': str, 'num_dep': int},
        'partition_by': 'num_dep', 'partition_init': 1, 'partition_end': 5, 'partition_interval': round(5 / 3)},
        'Departamento': {'columns-type': {'num': int, 'nome': str},
         'partition_by': 'num_dep', 'partition_init': 1, 'partition_end': 5, 'partition_interval': round(5 / 3)}
        }

        self.replica_count = 1
        
        self.add_neighbors()
        self.add_table()

        
    def add_neighbors(self):
        for db in self.cluster:
            copy = self.cluster.copy()
            copy.remove(db)
            db.add_neighbor(copy)

    def add_table(self):
        for db in self.cluster:
            db.add_table('Funcionário', self.dataframes['Funcionário']['columns-type'])
            db.add_table('Departamento', self.dataframes['Departamento']['columns-type'])

    def add_data(self, table, data: dict):
        partition_by = self.dataframes[table]['partition_by']
        partition_interval = self.dataframes[table]['partition_interval']
        partition_init = self.dataframes[table]['partition_init']

        number = data[partition_by]

        if 1 <= number <= 2:
            self.cluster[0].add_data(self.replica_count, table, data)
        elif 3 <= number <= 4:
            self.cluster[1].add_data(self.replica_count, table, data)
        elif number == 5:
            self.cluster[2].add_data(self.replica_count, table, data)








