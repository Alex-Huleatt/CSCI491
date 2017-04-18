import MySQLdb


def init_cursor():
    db = MySQLdb.connect("localhost", "root", "root", "nppes_db")
    cursor = db.cursor()
    return cursor


def updateRows(cursor, gener):

    cmd = 'INSERT INTO npi_organization_data %s' + \
        ' VALUES %s ON DUPLICATE KEY UPDATE'

    for g in gener:
        cursor.execute(cmd % g)


def completed_update(fname):
    pass


if __name__ == '__main__':
    print init_cursor()
