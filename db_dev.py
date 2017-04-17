import MySQLdb


def init_cursor():
    db = MySQLdb.connect("localhost", "root", "toor", "nppes_1")
    cursor = db.cursor()
    return cursor


def update(cursor, header, new_rows):
    cmd = 'INSERT INTO npi_organization_data asdasd' + \
        ' VALUES %s ON DUPLICATE KEY UPDATE'
    for row in new_rows:
        cursor.execute(cmd % row)


if __name__ == '__main__':
    print init_cursor()
