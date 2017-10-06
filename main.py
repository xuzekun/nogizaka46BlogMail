# coding=utf-8
from MainPageSpider import MainPageSpider
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from logger import logger
logging = logger().logging

def runNogizaka():
	logging.info('check update of nogizaka')
	spider = MainPageSpider()
	spider.run('nogizaka')

def runKeyakizaka():
	logging.info('check update of keyakizaka')
	spider = MainPageSpider()
	spider.run('keyakizaka')

def main():
	#spider = MainPageSpider()
	#spider.run()
	sched = BlockingScheduler()
	#sched.add_job(runNogizaka, 'interval', seconds=5, id='nogizaka')
	sched.add_job(runNogizaka, 'cron', minute='0,10,20,30,40,50', id='nogizaka')
	sched.add_job(runKeyakizaka, 'cron', minute='5,15,25,35,45,55', id='keyakizaka')
	sched.start()



if __name__ == '__main__':
	main()
	#url = 'http://blog.nogizaka46.com/misa.eto/2017/08/040435.php'
	# url = 'http://blog.nogizaka46.com/nanase.nishino/2017/09/041127.php'
	# spider = BlogSpider()
	# spider.run(url)
	# print spider.author
	# print spider.title
	# db = BlogDB()
	# db.connectdb()
	# db.createTable()
	# db.insertdb(url, spider.title, spider.author, spider.date)
	# res =  db.querydb(url)
	# if  res :
	# 	print res

