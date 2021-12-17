import sqlite3
import sys
sys.path.append('src/models')
sys.path.append('src/views')
from flask import Flask
from models import db
from views import app
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(daemon = True)

def tick1():
    sqliteConnection = sqlite3.connect('..//library.db')
    cursor = sqliteConnection.cursor()

    #Scrapped the implementation of automated lateness feature.
    '''where cast(("triggertime" - issuedt) as integer) > 1'''
    '''(borrows.issuedt + 1) > triggertime'''
    '''set late = 1, fine = 1 where cast((datetime.now(UTC) - issuedt) as integer) > 1'''
    '''lates = cursor.execute('library.db.filter(func.DATE(borrows.issuedt == date.today()))')'''
    '''cursor.execute(lates)'''
    '''sql = 'update borrows set late = 1 where date.today() == borrows.issuedt'
    cursor.execute(sql)'''

    sql = 'update Borrows set fine = fine + 0.01 where late = 1'
    cursor.execute(sql)
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()

sched.add_job(tick1,'interval',seconds=1)
sched.start()

run_app = Flask(__name__)
run_app.secret_key = b'testkey'
run_app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///../library.db'
run_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(run_app)
run_app.register_blueprint(app)

if __name__ == '__main__':
    run_app.run()