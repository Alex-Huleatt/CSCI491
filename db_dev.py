import MySQLdb


def init_cursor():
    db = MySQLdb.connect("localhost", "root", "root", "nppes_db")
    cursor = db.cursor()
    return cursor


def update(cursor, new_rows):
    cmd = 'INSERT INTO master_table' + \
        ' VALUES %s ON DUPLICATE KEY UPDATE'
    for row in new_rows:
        cursor.execute(cmd % row)


print init_cursor()
