import pandas as pd
from interface import *

from database import *


db1 = Database('db1')
db2 = Database('db2')
db3 = Database('db3')
#
# df1 = {'table_name': 'Funcionário', 'columns-type': {'cpf': str, 'nome': str, 'num_dep': int},
#        'partition_by': 'num_dep', 'partition_range': range(1, 5), 'partition_interval': round(5/3)}
# df2 = {'table_name': 'Departamento', 'columns-type': {'num': int, 'nome': str}}
# # funcionario = pd.DataFrame(columns=['cpf', 'nome', 'num_dep'])
# # departamento = pd.DataFrame(columns=['num', 'nome'])

cluster = [db1, db2, db3]


inter = Interface(cluster)

inter.add_data('Funcionário', {'cpf': '123445', 'nome': "Abelardo dos Santos", 'num_dep': 4})
# db1.add_neighbor([db2, db3])
# db2.add_neighbor([db1, db3])
# db3.add_neighbor([db1, db2])
#
#
#
# for db in cluster:
#     db.add_table(df1['table_name'], df1['columns-type'], )
#     db.add_table(df2['table_name'], df2['columns-type'], )
#
#     # print(db.data)
#
# replica_count = 1
#
#
#
# db1.add_data(replica_count, 'Funcionário', {'cpf': '123445', 'nome': "Abelardo dos Santos", 'num_dep': 4})
# db1.add_data(replica_count, 'Funcionário', {'cpf': '457899', 'nome': "Jailson Jr", 'num_dep': 3})
#
# db1.remove_data(replica_count, 'Funcionário', {'name': 'num_dep', 'operator': '==', 'param': 3})
# #eval(f"{name}{operator}{param}")
