# coding=utf-8

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import json
from logger import logger

class SendMail():
	def __init__(self):
		self.logging = logger().logging
		with open('etc/mailConfig.json', 'rb') as json_file:
			try:
				config = json.load(json_file)
				self.mailHost = config['mailHost']
				self.mailUser = config['mailUser']
				self.mailPasswd = config['mailPasswd']
				self.sender = config['sender']
				self.receivers = config['receivers']
				self.cc = config['cc']
				print 'mailConfig.json load succed'
			except Exception, e:
				print e

	def createMail(self, author, title, content):
		self.logging.info('creating the mail')
		self.message = MIMEMultipart()
		self.message['Subject'] = "[%s] %s" % (author, title)
		self.message['From'] = self.sender
		self.message['To'] = ','.join(self.receivers)
		self.message['Cc'] = ','.join(self.cc)

		#mail content
		text = MIMEText(content, 'html', 'utf-8')
		self.message.attach(text)


	def addAttach(self, picLists):
		for pic in picLists:
			print pic
			with open(pic, 'rb') as f:
				image = MIMEImage(f.read())
			s = pic.split('/')
			picName = (s[1] + '_' + s[2]).replace('/','_')
			self.logging.info('uploading the pic: %s' % picName)
			image['Content-Type'] = 'application/octet-stream'
			image['Content-Disposition'] = 'attachment;filename="%s"' % picName.encode('gb18030')
			self.message.attach(image)

	def send(self):
		try:
			smtpObj = smtplib.SMTP()
			smtpObj.connect(self.mailHost, 25)
			smtpObj.login(self.mailUser, self.mailPasswd)
			smtpObj.sendmail(self.sender, self.receivers + self.cc, self.message.as_string())
			smtpObj.quit()
			self.logging.info('send mail succeed!')
		except smtplib.SMTPException as e:
			print e

	def sendMail(self, author, title, content, picsList):
		try:
			self.createMail(author, title, content)
			self.addAttach(picsList)
			self.send()
			return True
		except Exception as e:
			return False

if __name__ == '__main__':
	mail = SendMail()
	html = '''
	<html>
	<head></head>
	<body>
	<div><a href='http://cdn.keyakizaka46.com/images/14/eaf/92d7a75061bbc03559d21d58fdceb.jpg'>aaa </a></div>
	<div>中秋快乐</div></body>
	</html>
	'''
	mail.sendMail(u'庆祝',u'中秋节快乐', html, [])
