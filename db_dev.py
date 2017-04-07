import MySQLdb


db = MySQLdb.connect("localhost", "root", "4ebb9q1", "nppes_1")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SHOW TABLES")

# Fetch a single row using fetchone() method.
data = cursor.fetchall()

print data
