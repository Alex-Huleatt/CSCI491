import web_parser
import csvParser
import db_dev as db



def main():
    print 'initialize database connection...'
    db.init()
    db.deactiv_update()
    db.close()
    print 'exit'
    

if __name__ == '__main__':
    main()
