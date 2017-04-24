import web_parser
import csvParser
import db_dev as db



def main():
    print 'initialize database connection...'
    db.init()
    print 'get download links...'
    dl_links = web_parser.get_download_links()
    toUse = db.filterFiles(dl_links)
    print '%s new update files.' % len(toUse)
    for f in toUse:
        print 'retrieve csv %s...' % f
        csv_name = web_parser.retrieve_csv_file(f)
        print 'parse csv...'
        up = csvParser.CSV2(csv_name)
        print 'load headers...'
        headers = csvParser.loadHeaders('header.csv')
        print 'update db...'
        db.update(headers, up)
        db.completed_update(f)
    print 'closing connection...'
    db.close()
    print 'exit'
    

if __name__ == '__main__':
    main()
