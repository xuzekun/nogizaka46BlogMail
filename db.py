#!/usr/bin/env python
# coding=utf-8
import MySQLdb
import json

class DB():
    def __init__(self):
        with open('dbConfig.json','rb') as json_file:
            try:
                config = json.load(json_file)
                self.host = config['host']
                self.port = config['port']
                self.user = config['user']
                self.passwd = config['passwd']
                self.dbname = config['dbname']
            except ValueError, err:
                print "dbConfig.json parse error"
                print err


    def connectdb(self):
        try:
            self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.dbname, charset='utf8')
        except Exception, e:
            print e

    def createTable(self, cmd):
        cursor = self.db.cursor()
        cursor.execute(cmd)

    def insertdb(self, cmd):
        cursor = self.db.cursor()
        try:
            cursor.execute(cmd)
            self.db.commit()
        except Exception, e:
            print e
            self.db.rollback()

    def querydb(self, cmd):
        cursor = self.db.cursor()
        try:
            cursor.execute(cmd)
            results = cursor.fetchall()
        except Exception, e:
            print e

        return results

    def updatedb(self, cmd):
        cursor = self.db.cursor()
        try:
            cursor.execute(cmd)
            self.db.commit()
        except Exception, e:
            print e 
            self.db.rollback()

    def deletedb(self, cmd):
        cursor = self.db.cursor()
        try:
            cursor.execute(cmd)
            self.db.commit()
        except Exception, e:
            print e
            self.db.rollback()

    def close(self):
        self.db.close()



if __name__ =='__main__':
    db = BlogDB()
    db.connectdb()
    results = db.querydb("select * from BLOG")
    for row in results:
        print row[1]
    print db.host
    print db.port
