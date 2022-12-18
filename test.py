import pandas as pd
from interface import *

from database import *

import MySQLdb
import credentials

# conn: MySQLdb.Connection = MySQLdb.connect(
#     host=credentials.hostname,
#     user=credentials.username,
#     passwd=credentials.password
# )
#
# for i in range(1, 4):
#     with conn.cursor() as cursor:
#         cursor.execute(f'CREATE SCHEMA `db{i}` ;')

schemas = ['db1', 'db2', 'db3']

db1 = Database('db1')
db2 = Database('db2')
db3 = Database('db3')

cluster = [db1, db2, db3]


inter = Interface(cluster)

#db1.add_data(1, "")

r1, r2 = db1.get_data()

print(r1, r2)
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
