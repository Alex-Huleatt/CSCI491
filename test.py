
import autocross as ac
import db_dev as db

db.init()
ac.clear_db(None)
ac.auto(None)
ac.deact(None)
db.close()