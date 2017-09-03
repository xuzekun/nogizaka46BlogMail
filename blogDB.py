#!/usr/bin/env python
# coding=utf-8
import MySQLdb
import json
from db import DB

class BlogDB(DB):
    def __init__(self):
        DB.__init__(self)

    def checkTableExists(self):
        cursor = self.db.cursor()
        cmd = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='BLOG'"
        cursor.execute(cmd)
        if cursor.fetchone()[0] == 1:
            return True
        return False

    def createTable(self):
        if self.checkTableExists() is False:
            cursor = self.db.cursor()
            cmd = '''
                create table if not exists BLOG(
                url VARCHAR(128) NOT NULL PRIMARY KEY,
                title TEXT,
                author TEXT,
                date DATETIME
                )character set utf8; 
            '''     
            cursor.execute(cmd)


    def insertdb(self, url, title, author, date):
        cursor = self.db.cursor()
        cmd = "INSERT INTO BLOG (url, title, author, date) VALUES ('%s', '%s', '%s', '%s');" %(url, title, author, date)
        try:
            cursor.execute(cmd)
            self.db.commit()
        except Exception, e:
            print e
            self.db.rollback()

    def querydb(self, url):
        cursor = self.db.cursor()
        cmd = "SELECT * from BLOG WHERE url='%s'" % url
        try:
            cursor.execute(cmd)
            results = cursor.fetchall()
            return results
        except Exception, e:
            print e

    




if __name__ =='__main__':
    db = BlogDB()
    db.connectdb()
    db.createTable()
    db.insertdb("http://www.123.com", "い肆拾贰", "ddd试试", "2017/07/21 18:48")
    #db.insertdb("http://www.123.com", "い肆拾贰", "ddd试试", "2017-06-06 12:13:14")
    results = db.querydb("http://www.123.com")
    for row in results:
        print row[1]
    print db.host
    print db.port
    db.updatedb("update BLOG SET author='u' WHERE url='http://www.nogizaka.com/'")
    db.deletedb("delete FROM BLOG WHERE url='http://423www.nogizaka.com/'")
    db.close()

