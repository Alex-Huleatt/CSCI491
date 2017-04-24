import MySQLdb, datetime

cursor = None

def init():
    global cursor
    cursor = init_cursor()

def init_cursor():
    db = MySQLdb.connect("localhost", "root", "toor", "nppes_1")
    db.autocommit(True)
    cursor = db.cursor()
    return cursor

def update(head_map, headers, gener):
    cmd = 'REPLACE INTO %s \n(%s)\n VALUES(%s);'
    org = 'npi_organization_data'
    prv = 'npi_provider_data'
    
    for g in gener:
        try:
            prsed = parseRow(head_map, headers, g)
            keys, vals = '', ''
            val_f = '"%s",'
            for k,v in prsed.iteritems():
                keys += k + ','
                vals += val_f % v
            keys = keys[:-1] # cut off extra comma
            vals = vals[:-1] # cut off extra comma
            table = org if g[1]!='1' else prv
            toExec = cmd % (table, keys, vals) 
            cursor.execute(toExec)
        except Exception as e:
            print e


def parseRow(head_map, headers, row):
    ret = {}
    for k in range(len(headers)):
        if headers[k] in head_map:
            if head_map[headers[k]] == 'DeactivationDate':
                if row[k] == '':
                    continue
                else:
                    ret[head_map[headers[k]]] = datetime.datetime.strptime(row[k],'%m/%d/%Y')
            else:
                ret[head_map[headers[k]]] = row[k]
    return ret

def completed_update(fname):
    try:
        cursor.execute("INSERT INTO used_files (file_name) VALUES('%s');" % fname)
    except Exception as e:
        print e

def filterFiles(ls):
    cursor.execute('SELECT * FROM used_files')
    res = [r[0] for r in cursor.fetchall()]
    return filter(lambda x:x not in res, ls)

def close():
    global cursor
    cursor.close()

if __name__ == '__main__':
    init()
    filterFiles([])
