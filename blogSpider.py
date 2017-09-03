# coding=utf-8

import requests
from lxml import html

class BlogSpider():
	def __init__(self):
		self.htmlPage = ""
		self.author = ""
		self.title = ""
		

	def getHtml(self, url, retryNum=5):
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
		rsp = requests.get(url, headers=headers)
		if rsp.status_code == 200:
			return rsp.content
		else:
			if retryNum > 0:
				print "retry"
				self.getHtml(url, retryNum-1)
		print 1

	def extraInfo(self, xpath):
		tree = html.fromstring(self.htmlPage)
		lists = tree.xpath(xpath)
		return lists[0]


	def extraContent(self):
		tree = html.fromstring(self.htmlPage)
		lists = tree.xpath('//*[@id="sheet"]/div[2]/div')
		content = ""

		for div in lists:
			content += html.tostring(div, method='html', encoding='utf-8')

		head = "<html><head></head><body>"
		tail = "</body></html>"
		content = head + content + tail
		return content


	def run(self, url):
		self.htmlPage = self.getHtml(url)
		if self.htmlPage is not None:
			self.title = self.extraInfo('//span[@class="entrytitle"]/text()')
			self.author = self.extraInfo('//span[@class="author"]/text()')
			self.date = self.extraInfo('//*[@id="sheet"]/div[3]/text()')
			self.content = self.extraContent()
		else:
			print "pageNone"

# tree = html.fromstring(rsp.content)
# lists = tree.xpath('//*[@id="sheet"]/div[2]/div')

# #print lists[0].text.encoding('gbk')
# htmlPage = ""
# for li in lists:
# 	div = html.tostring(li,method='html',encoding='utf-8')
# 	htmlPage += div

# print htmlPage


if __name__ == '__main__':
	spider = BlogSpider()
	htmlPage = spider.run('http://blog.nogizaka46.com/misa.eto/2017/08/040435.php')

