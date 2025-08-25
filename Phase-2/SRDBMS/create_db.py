import sqlite3


def create_db():
    con = sqlite3.connect(databse="rms.db")
    cur = con.cursor()
    cur.execute("CREATE TALE IF NOT EXIXTS course(cid INTEGER PRIMARY KEY AUTOINCREMENT,course text,duration text,charges teext, description text)")
    con.commit()


create_db()
