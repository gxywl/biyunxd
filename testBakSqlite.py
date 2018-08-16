# _*_ encoding: utf-8 _*_
import sqlite3

def testBakSqlite():
    conn = sqlite3.connect("data-dev.sqlite")
    with open('data-dev.sql.bak','w') as f:
        for line in conn.iterdump():
            data = line + '\n'
            data = data.encode("utf-8")
            f.write(data)
			
testBakSqlite()