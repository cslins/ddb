import MySQLdb

hostname = 'localhost'
username = 'chuu'
password = 'queime666facomp666imediatamente'
database = 'dbname'

conn = MySQLdb.connect(
    host=hostname,
    user=username,
    passwd=password,
    db=database
)

cursor = conn.cursor()

cursor.execute("SELECT fname, lname FROM employee")

for firstname, lastname in cursor.fetchall():
    print(firstname, lastname)

conn.close()
