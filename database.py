import pandas as pd


class Database:
    def __init__(self, name: str):
        self.name: str = name
        self.data: dict = {}
        self.metadata: dict = {}
        self.neighbors: list = []

    def add_neighbor(self, neighbors):
        for database in neighbors:
            self.neighbors.append(database)

    def add_table(self, table_name, columns_type):
        df: pd.DataFrame = pd.DataFrame(columns=columns_type.keys())
        self.data[table_name] = df

        for k, v in columns_type.items():
            df[k] = df[k].astype(v)

        print(table_name, 'adicionada em', self.name)

    def add_data(self, replication_count, table, data: dict):
        self.data[table] = pd.concat([self.data[table], pd.DataFrame([data])], axis=0)
        # self.data[table] = self.data[table].append(data, ignore_index=True)
        print(self.name, "\n", self.data[table])

        # comunicação
        if replication_count > 0:
            self.neighbors[0].add_data(replication_count-1, table, data)

    def remove_data(self, table, data: dict, condition=None):
        pass

    def update_data(self, table, data: dict, condition=None):
        pass

    def select_data(self, table, columns: list, condition=None):
        pass

    def get_data(self):
        return self.data

    def send_data(self, database):
        pass
