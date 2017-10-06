# coding=utf-8

import requests
from lxml import html
import os
from logger import logger

class BlogSpider():
	def __init__(self):
		self.htmlPage = ""
		self.author = ""
		self.title = ""
		self.logging = logger().logging

	def getHtml(self, url, retryNum=5):
		self.logging.info('get url begin: %s' % url)
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
		try:
			rsp = requests.get(url, headers=headers, timeout=20)
		except Exception as e:
			self.logging.info(e)
			self.logging.info('get failed')
			if retryNum > 0:
				self.logging.info('get url: %s fail and retryNum=%d !' % (url, retryNum))
				return self.getHtml(url, retryNum - 1)

		self.logging.info('get url end: %s' % url)
		if rsp.status_code == 200:
			self.logging.info('get url: %s succeed!' % url)
			self.logging.debug(rsp.content)
			return rsp.content
		else:
			self.logging.info('get rspcode != 200')
			if retryNum > 0:
				self.logging.info('get url: %s fail and retryNum=%d !' % (url, retryNum))
				return self.getHtml(url, retryNum-1)

	def extraInfo(self, htmlPage, xpath):
		tree = html.fromstring(htmlPage)
		lists = tree.xpath(xpath)
		if len(lists) == 1:
			return lists[0]
		return lists


	def extraContent(self, htmlPage ,xpath):
		tree = html.fromstring(htmlPage)
		lists = tree.xpath(xpath)
		content = ""

		for div in lists:
			content += html.tostring(div, method='html', encoding='utf-8')

		head = "<html><head></head><body>"
		tail = "</body></html>"
		content = head + content + tail
		return content

	def downloadPic(self, htmlPage):
		localImgs = []
		saveDir = 'Pic/' + self.author + '/'
		saveNamePrefix = str(self.date).split()[0].replace('/', '') + '_' + self.title + '_'
		if not os.path.exists(saveDir):
			os.makedirs(saveDir)

		picsList = self.extraInfo(htmlPage, '//*[@id="sheet"]/div[2]/div/a/@href')
		num = 0
		for picUrl in picsList:
			if not picUrl.startswith('http://dcimg.awalker.jp'):
				continue
			session = requests.session()
			img1Page = session.get(picUrl).content
			realPicUrl = self.extraInfo(img1Page, '//*[@id="contents"]/img/@src')
			self.logging.info('downloading the pic: %s' % realPicUrl)
			img2 = session.get(realPicUrl, stream=True)
			num = num + 1
			localImg = saveDir + saveNamePrefix + str(num)+ '.jpg'
			localImgs.append(localImg)
			with open(localImg, 'wb') as f:
				for chunk in img2.iter_content():
					f.write(chunk)
		return localImgs

	def downloadKeyakizakaPic(self, htmlPage):
		localImgs = []
		saveDir = 'Pic/' + self.author + '/'
		saveNamePrefix = str(self.date).replace('/', '').replace(':', '') + '_'
		if not os.path.exists(saveDir):
			os.makedirs(saveDir)

		picsList = self.extraInfo(htmlPage, '//div[@class="box-article"]//img/@src')
		num = 0
		for picUrl in picsList:
			if not picUrl.startswith('http://cdn.keyakizaka46.com'):
				continue
			self.logging.info('downloading the pic: %s' % picUrl)
			session = requests.session()
			img2 = session.get(picUrl, stream=True)
			num = num + 1
			localImg = saveDir + saveNamePrefix + str(num) + '.jpg'
			localImgs.append(localImg)
			with open(localImg, 'wb') as f:
				for chunk in img2.iter_content():
					f.write(chunk)
		return localImgs

	def runNogizaka(self, url):
		self.logging.info('run Nogizaka begin')
		self.htmlPage = self.getHtml(url)
		if self.htmlPage is not None:
			self.title = self.extraInfo(self.htmlPage, '//span[@class="entrytitle"]/text()')
			self.author = self.extraInfo(self.htmlPage, '//span[@class="author"]/text()')
			self.date = self.extraInfo(self.htmlPage, '//*[@id="sheet"]/div[3]/text()')
			self.content = self.extraContent(self.htmlPage, '//*[@id="sheet"]/div[2]/div')
			self.picsList = self.downloadPic(self.htmlPage)
		else:
			print "pageNone"

	def runKeyakizaka(self, url):
		self.logging.info('run keyyakizaka begin')
		self.htmlPage = self.getHtml(url)
		if self.htmlPage is not None:
			title = self.extraInfo(self.htmlPage, '//article/div[1]/div[2]/h3/text()')
			self.title = title.strip()
			author = self.extraInfo(self.htmlPage, '//article/div[1]/div[2]/p/a/text()')
			self.author = author.strip().strip(' ')
			date = self.extraInfo(self.htmlPage, '//article/div[3]/ul/li/text()')
			self.date = date.strip()
			self.content = self.extraContent(self.htmlPage, '//article/div[2]')
			self.picsList = self.downloadKeyakizakaPic(self.htmlPage) #//div[@class='box-article']//img/@src
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
	#htmlPage = spider.run('http://blog.nogizaka46.com/mai.shinuchi/2017/09/040550.php')
	#spider.runKeyakizaka('http://www.keyakizaka46.com/s/k46o/diary/detail/11852?ima=0000&cd=member')
	spider.runKeyakizaka('http://www.keyakizaka46.com/s/k46o/diary/detail/11885?ima=0000&cd=member')
	print spider.content



