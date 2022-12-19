from database import *
import MySQLdb


class Interface:
    def __init__(self, clusters: list): #, conn: MySQLdb.Connection):
        self.clusters = clusters

        self.dataframes = {
        'Funcionario': {'columns-type': {'id': int, 'nome': str, 'cpf': str,'n_departamento': int}},
        'Departamento': {'columns-type': {'id': int, 'nome': str}}
        }

        self.replica_count = 1
        self.query = ""
        query = """
                INSERT INTO funcionario (id, nome)
                VALUES
                    (4, "Fabiola"),
                    (5, "Quites")
                
                """
        #self.rcv_query(query)

    # ..
    def rcv_query(self, query):
        self.query: str = query
        temp_query = query.lower()
        table: str

        if temp_query.__contains__(" departamento"):
            table = "departamento"
        elif temp_query.__contains__("funcionario"):
            table = "funcionario"
        else: return

        if temp_query.__contains__("insert"):
            self.add_data(table, self.query)
        elif temp_query.__contains__("delete"):
            self.remove_data(table, self.query)
        elif temp_query.__contains__("update"):
            self.update_data(table, self.query)
        elif temp_query.__contains__("select"):
            return self.select_data(table, self.query)

        #state_query = f"""SELECT * FROM {table}"""

        return {}



    def add_neighbors(self):
        for db in self.clusters:
            copy = self.clusters.copy()
            copy.remove(db)
            db.add_neighbor(copy)

    def add_data(self, table, query):
        query_broken: list[str] = query.split("VALUES")  # ["INSERT INTO", "()\n()\n()"]
        print(query_broken)

        insert_into = query_broken[0].split(table)[1].strip()
        insert_into = insert_into.removeprefix('(').removesuffix(')')
        attributes = insert_into.replace(" ", "").split(",")
        print(attributes)

        values = query_broken[1].split("),")
        print(values)
        values_extracted = [v.strip().replace(" ", "").removeprefix("(").removesuffix(")").split(',') for v in values]
        print(values_extracted)
        values_needed = [v for v in values_extracted if len(v) == len(attributes)]
        print(values_needed)
        values_clean = [i.replace('\"', '') for v in values_needed for i in v]

        dict_op = {
            "table": table,
            "attributes": attributes,
            "values": values_needed
        }

        self.clusters[0].add_data(self.replica_count, dict_op)


    def remove_data(self, table, query):
        temp_query = query.upper()
        if temp_query.__contains__("WHERE"):
            query_broken: list[str] = query.split("WHERE")
            print(query_broken)

            # operators = ['<>', '<=', '=>', '<', '>', '=']
            # op = ''
            #
            # for o in operators:
            #     if query_broken[1].__contains__(o):
            #         op = o
            #         break

            query_condition = query_broken[1].strip()
            # query_condition_list = query_condition.split(op)
            print(query_condition)
            # column = query_condition_list[0].strip()
            # param = query_condition_list[1].strip()

            condition = {'string': query_condition}
            self.clusters[0].remove_data(0, table, condition, replica=False)

        else:
            self.clusters[0].remove_data(0, table, replica=False)


    def update_data(self, table, query):
        temp_query = query.upper()
        if temp_query.__contains__("WHERE"):
            query_broken: list[str] = query.split("WHERE")
            print(query_broken)

            query_set = query_broken[0].split("SET")[1].strip()
            query_condition = query_broken[1].strip()

            # query_condition_list = query_condition.split(op)
            print(query_set)
            print(query_condition)
            # column = query_condition_list[0].strip()
            # param = query_condition_list[1].strip()

            condition = {'set': query_set, 'where': query_condition}
            self.clusters[0].update_data(0, table, condition, replica=False)

        else:
            query_broken: list[str] = query.split("SET")
            query_set = query_broken[1].strip()
            print(query_set)
            condition = {'set': query_set, 'where': None}
            self.clusters[0].update_data(0, table, condition, replica=False)

    def select_data(self, table, query):
        temp_query = query.upper()

        # there is a where clause
        if temp_query.__contains__("WHERE"):
            query_broken: list[str] = query.split("WHERE")
            print(query_broken)

            atributes = query_broken[0].split("SELECT")[1].split("FROM")[0].strip()
            attr = atributes.split(",")
            print(atributes)

            query_condition = query_broken[1].strip()
            print(query_condition)

            condition = {'string': query_condition}
            r = self.clusters[0].select_data(table, atributes, condition, False)
            print(r)
            return self.organize(r, attr, table)
        # there is no where clause
        else:
            atributes = query.split("SELECT")[1].split("FROM")[0].strip()
            attr = atributes.split(",")
            attr = [a for a in attr]
            print(attr)
            print(atributes)
            r = self.clusters[0].select_data(table, atributes, replica=False)
            print(r)
            return self.organize(r, attr, table)


    #..
    def select_all_database(self):

        return {'db1': self.select_data_by_database(0),
                'db2': self.select_data_by_database(1),
                'db3': self.select_data_by_database(2)}




    def select_data_by_database(self, db: int):
        func, dep = self.clusters[db].get_data()

        atr_func = list(self.dataframes['Funcionario']['columns-type'].keys())
        print()

        print(f"Atr_func: {atr_func}")
        dic = {}
        for i in range(len(atr_func)):
            dic[atr_func[i]] = []
            for n in range(len(func)):
                dic[atr_func[i]].append(func[n][i])

        print(dic)

        d = {'Funcionario': dic}

        atr_dep = list(self.dataframes['Departamento']['columns-type'].keys())
        print()

        print(f"Atr_dep: {atr_dep}")
        dic2 = {}
        for i in range(len(atr_dep)):
            dic2[atr_dep[i]] = []
            for n in range(len(dep)):
                dic2[atr_dep[i]].append(dep[n][i])

        print(dic2)

        d['Departamento'] = dic2

        print(d)

        return d

    # ..
    def select_all(self):
        return dict

    def organize(self, lista, atr, table):
        print(lista)

        flattened = [item for sublist in lista for item in sublist]
        print("f", flattened)

        nova = []
        for elem in flattened:
            if elem not in nova:
                nova.append(elem)

        print(f"Nova: {nova}")
        dic = {}

        print(f"Atr: {atr}")

        for i in range(len(atr)):
            dic[atr[i]] = []
            for n in range(len(nova)):
                dic[atr[i]].append(nova[n][i])

        print(dic)

        d = {table: dic}

        print(d)

        return d















