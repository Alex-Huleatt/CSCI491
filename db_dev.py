import MySQLdb, datetime
import web_parser as wp
import csvParser as csv
import xlsx_parser as xlsx
import re

cursor = None

head_map = {'Provider License Number_1': 'LicenseNumber1',
                'Provider Organization Name (Legal Business Name)': 'Name',
                'Is Organization Subpart': 'IsOrganizationSubpart',
                'Authorized Official Credential Text': 'AuthorizedOfficialCredential',
                'Provider Second Line Business Mailing Address': 'SecondLineMailingAddress',
                'Authorized Official Last Name': 'AuthorizedOfficialLastName',
                'Authorized Official First Name': 'AuthorizedOfficialFirstName',
                'Provider Business Mailing Address Postal Code': 'MailingAddressPostalCode',
                'Provider Business Practice Location Address City Name': 'PracticeAddressCity',
                'Is Sole Proprietor': 'IsSoleProprietor',
                'Authorized Official Telephone Number': 'AuthorizedOfficialTelephone',
                'Provider Business Mailing Address Country Code (If outside U.S.)': 'MailingAddressCountryCode',
                'Provider Other Organization Name': 'OtherName',
                'Provider Business Practice Location Address State Name': 'PracticeAddressState',
                'Provider Business Mailing Address Telephone Number': 'MailingAddressTelephone',
                'Provider Business Mailing Address Fax Number': 'MailingAddressFax',
                'Provider First Line Business Mailing Address': 'FirstLineMailingAddress',
                'Authorized Official Title or Position': 'AuthorizedOfficialTitle',
                'Healthcare Provider Taxonomy Code_1': 'TaxonomyCode1',
                'Provider Business Practice Location Address Postal Code': 'PracticeAddressPostalCode',
                'NPI Deactivation Date': 'DeactivationDate',
                'Provider First Line Business Practice Location Address': 'FirstLinePracticeAddress',
                'Provider Second Line Business Practice Location Address': 'SecondLinePracticeAddress',
                'NPI': 'NPI',
                'Provider Business Practice Location Address Telephone Number': 'PracticeAddressTelephone',
                'Provider Business Mailing Address City Name': 'MailingAddressCity',
                'Provider Business Practice Location Address Fax Number': 'PracticeAddressFax',
                'Provider Other Organization Name Type Code': 'OtherNameTypeCode',
                'Provider Business Mailing Address State Name': 'MailingAddressState',
                'Provider License Number State Code_1': 'LicenseStateCode1',
                'Provider Business Practice Location Address Country Code (If outside U.S.)': 'PracticeAddressCountryCode',
                'Healthcare Provider Primary Taxonomy Switch_1': 'TaxonomySwitch1'}

def init():
    global cursor
    cursor = init_cursor()

def init_cursor():
    db = MySQLdb.connect("localhost", "root", "toor", "nppes_1")
    db.autocommit(True)
    cursor = db.cursor()
    return cursor
org = 'npi_organization_data'
prv = 'npi_provider_data'

def update(headers, gener):
    cmd = 'REPLACE INTO %s \n(%s)\n VALUES(%s);'
    
    
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
            raise e


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

def update_deactivation(d_list):
    
    cmd = "UPDATE %s SET %s.DeactivationDate=%s WHERE %s.NPI=%s;"
    for k in d_list:
        npi,dt = k[0],k[1]
        datetime.datetime.strptime(dt,'%m/%d/%Y')
        cursor.execute(cmd % (prv, prv, dt, prv, npi))
        cursor.execute(cmd % (org, org, dt, org, npi))


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



def _test():
    from csvParser import CSV2, loadHeaders
    init()
    test_csv = CSV2('testcsv.csv')
    h = loadHeaders('header.csv')
    update(h, test_csv)
    close()

def weekly_update():
    dl_links = wp.get_download_links()
    toUse = filterFiles(dl_links)
    print '%s new update files.' % len(toUse)
    print 'load headers...'
    headers = csv.loadHeaders('header.csv')
    for f in toUse:
        print 'retrieve csv %s...' % f
        csv_name = wp.retrieve_file(f)
        print 'parse csv...'
        up = csv.CSV2(csv_name)
        print 'update db...'
        update(headers, up)
        completed_update(f)

def deactiv_update():
    link = wp.get_download_links(reg=wp.deactiv_regex)[0]
    if len(filterFiles([link]))==0:
        print 'no new'
        return
    print 'retrieve xlsx %s...' % link
    name = wp.retrieve_file(link, reg=wp.xslx_regex)
    print 'parse xlsx...'
    up = xlsx.readxlsx(name)
    print 'update db...'
    update_deactivation(up)
    completed_update(link)

'''execute arbitrary sql file'''
'''taken from: http://stackoverflow.com/questions/4408714/execute-sql-file-with-python-mysqldb'''
def exec_sql_file(sql_file):
    print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                cursor.execute(statement)
            except Exception as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))

            statement = ""

def db_reset():
    print 'reset db'
    exec_sql_file('nppes_schema.sql')

def full_db():
    
    print 'get download link'
    link = wp.get_download_links(reg=wp.monthly_regex)[0]
    print 'download monthly.'
    csv_name = wp.retrieve_file(link)
    up = csv.CSV2(csv_name)
    print 'load headers...'
    headers = csv.loadHeaders('header.csv')
    update(headers, up)



