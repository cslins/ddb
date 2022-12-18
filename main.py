import MySQLdb
import pandas as pd

hostname = 'localhost'
username = 'chuu'
password = 'chuudid911'
database = 'db1'

conn: MySQLdb.Connection = MySQLdb.connect(
    host=hostname,
    user=username,
    passwd=password,
    db=database
)
cursor = conn.cursor()

# create multiple databases
# for i in range(0, 2):
#     conn: MySQLdb.Connection = MySQLdb.connect(
#         host=hostname,
#         user=username,
#         passwd=password
#     )
#     cursor = conn.cursor()
#
#     cursor.execute(f'CREATE SCHEMA `empresa{i}` ;')


# create multiple tables
for i in range(0, 2):

    conn: MySQLdb.Connection = MySQLdb.connect(
        host=hostname,
        user=username,
        passwd=password,
        db=f"db{i+1}"
    )

    cursor = conn.cursor()

    # create tables
    cursor.execute(
     """
    CREATE TABLE departamento(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100)
    )
    """
    )
    cursor.execute(
     """
    CREATE TABLE funcionario(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        cpf VARCHAR(11),
        n_departamento INT,
        FOREIGN KEY (n_departamento) REFERENCES departamento(id)
    )
    """
    )

# select
# cursor.execute("SELECT id, nome FROM departamento")
# print(cursor.fetchall())
# for id, nome in cursor.fetchall():
#     print(id, nome)

# insert
# cursor.execute(
# """
# INSERT INTO departamento (id, nome)
# VALUES
#     (1, "Memes"),
#     (2, "Administrativo"),
#     (3, "Financeiro"),
#     (4, "Memes"),
#     (5, "Administrativo"),
#     (6, "Financeiro"),
#     (7, "Memes"),
#     (8, "Administrativo"),
#     (9, "Financeiro"),

# """
# )
# conn.commit()

# delete
# cursor.execute(
# """
# DELETE FROM departamento
# """
# )
# conn.commit()

conn.close()
