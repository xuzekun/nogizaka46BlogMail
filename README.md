定时爬去[乃木坂nogizaka](http://blog.nogizaka46.com/)和[榉板keyakizaka](http://www.keyakizaka46.com/s/k46o/diary/member/list)的博客，下载图片，并自动发送邮件。

定时任务可在MainPageSpider.py里设置，目前是10分钟一次

sched.add_job(runNogizaka, 'cron', minute='0,10,20,30,40,50', id='nogizaka')

运行run:

python main.py

