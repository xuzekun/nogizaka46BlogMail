# coding = utf-8
from blogSpider import BlogSpider
from logger import logger
from blogDB import BlogDB
from sendMail import SendMail

class MainPageSpider():
    def __init__(self):
        self.logging = logger().logging
        self.db = BlogDB()
        self.db.connectdb()

    def getNewBlogList(self, flag):
        pageSpider = BlogSpider()
        finish = False
        pageIndex = 0
        newBlogUrls = []
        while True:
            if flag == 'nogizaka':
                mainPage = pageSpider.getHtml('http://blog.nogizaka46.com/?p=' + str(pageIndex+1))
                blogUrls = pageSpider.extraInfo(mainPage, '//*[@id="sheet"]/h1/span/span/a/@href')
                self.logging.info('the blogUrl of page %d is %s' % (pageIndex+1, blogUrls))
            elif flag == 'keyakizaka':
                mainPage = pageSpider.getHtml('http://www.keyakizaka46.com/s/k46o/diary/member/list?ima=0000&page=%d&cd=member' % pageIndex)
                urls = pageSpider.extraInfo(mainPage, '//article/div[1]/div[2]/h3/a/@href')
                blogUrls = []
                for url in urls:
                    blogUrls.append('http://www.keyakizaka46.com' + url)
                self.logging.info('the blogUrl of page %d is %s' % (pageIndex, blogUrls))
            else:
                self.logging.error('getNewBlogList flag error!')

            for url in blogUrls:
                ret = self.db.querydb(url)
                if len(ret) == 0:
                    newBlogUrls.insert(0, url)
                else:
                    finish = True
                    break

            if finish == True or pageIndex >= 0:
                break
            else:
                pageIndex += 1
        self.logging.info('the newBlogUrls is %s' % newBlogUrls)
        if len(newBlogUrls) > 2:
            newBlogUrls = newBlogUrls[0:2]
            self.logging.info("the blogUrls update this turn is %s" % newBlogUrls)

        return newBlogUrls

    def getBlogAndSendMail(self, urls, flag):
        for url in urls:
            self.logging.info('download blog begin: %s' % url)
            spider = BlogSpider()
            if flag == 'nogizaka':
                spider.runNogizaka(url)
            elif flag == 'keyakizaka':
                spider.runKeyakizaka(url)
            else:
                self.logging.error('getBlogAndSendMail error')
            mail = SendMail()
            result = mail.sendMail(spider.author, spider.title, spider.content, spider.picsList)
            if result:
                self.logging.info('send Mail [%s]%s succeed!' %(spider.author, spider.title))
                # write database
                self.db.insertdb(url, spider.title, spider.author, spider.date)
                self.logging.info('write db succeed!')

    def run(self, flag):
        newBlogUrls = self.getNewBlogList(flag)
        self.getBlogAndSendMail(newBlogUrls, flag)


if __name__ == '__main__':
    pageSpider = MainPageSpider()
    #pageSpider.run('nogizaka')
    pageSpider.run('keyakizaka')

