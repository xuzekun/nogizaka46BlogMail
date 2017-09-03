# coding=utf-8
from blogSpider import BlogSpider
from blogDB import BlogDB


if __name__ == '__main__':
	url = 'http://blog.nogizaka46.com/misa.eto/2017/08/040435.php'
	spider = BlogSpider()
	spider.run(url)
	db = BlogDB()
	db.connectdb()
	db.createTable()
	db.insertdb(url, spider.title, spider.author, spider.date)
	res =  db.querydb("url")
	if not res :
		print "none"

