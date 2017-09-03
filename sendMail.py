# -*- coding:utf8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import json

class SendMail():
	def __init__(self):
		with open('mailConfig.json', 'rb') as json_file:
			try:
				config = json.load(json_file)
				self.mailHost = config['mailHost']
				self.mailUser = config['mailUser']
				self.mailPasswd = config['mailPasswd']
				self.sender = config['sender']
				self.receivers = config['receivers']
				print 'mailConfig.json load succ'
			except Exception, e:
				print e

	def createMail(self, author, title, content):
		self.message = MIMEMultipart()
		self.message['Subject'] = "[%s] %s" % (author, title)
		self.message['From'] = self.sender
		self.message['To'] = ','.join(self.receivers)

		#mail content
		text = MIMEText(content, 'html', 'utf-8')
		self.message.attach(text)


	def addAttach(self, picLists):
		for pic in picLists:
			print pic
			with open(pic, 'rb') as f:
				image = MIMEImage(f.read())
			image['Content-Type'] = 'application/octet-stream'
			image['Content-Disposition'] = 'attachment;filename="%s"' % pic
			self.message.attach(image)

	def send(self):
		try:
			smtpObj = smtplib.SMTP()
			smtpObj.connect(self.mailHost, 25)
			smtpObj.login(self.mailUser, self.mailPasswd)
			smtpObj.sendmail(self.sender, self.receivers, self.message.as_string())
			smtpObj.quit()
			print "send mail succ"
		except smtplib.SMTPException as e:
			print e

	def sendMail(self, author, title, content, picLists):
		self.createMail(title, content)
		self.addAttach(picLists)
		self.send()

if __name__ == '__main__':
	mail = SendMail()
	html = '''
	<html>
	<head></head>
	<body>
	<div><a href="http://img.nogizaka46.com/blog/misa.eto/img/2017/07/21/3017690/0000.jpeg"><img title="null" src="cid:0"></a></div>
	<div>どの位置にいても変わらずにずっと応援してくれるファンの皆さんに、感謝の気持ちでいっぱいです！</div></body>
	</html>
	'''
	mail.sendMail('a new mail', html, ['001.jpg'])
