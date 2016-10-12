import requests
from bs4 import BeautifulSoup
'''
分析贴吧发帖
'''
class getinfor(object):

    # 得到源html代码。
    def gethtml(self,url):
        retu = requests.post(url)
        return retu.content.decode('utf-8')
    # 处理源代码
    def chuli(self,html):
        soup = BeautifulSoup(html,'lxml')
        list_ul = soup.find_all('ul',attrs={'id':'thread_list','class':'threadlist_bright j_threadlist_bright'})
        return list_ul

g = getinfor()
url='http://tieba.baidu.com/f?kw=bilibili&fr=index&fp=0&ie=utf-8'
html = g.gethtml(url)
list_ul = g.chuli(html)
count = 0
for i in list_ul:
    for j in i.find_all('li',attrs={'class':' j_thread_list clearfix'}):
        # print(j)
        print('回复数：'+j.find_all('span',attrs={'title':'回复'})[0].text)
        print('标题：'+j.find_all('a',attrs={'class':'j_th_tit'})[0].text)
        print('作者：'+j.find_all('span',attrs={'class':'frs-author-name-wrap'})[0].text)
        print('发布时间：'+j.find_all('span',attrs={'class':'pull-right'})[0].text)
        print('内容：'+j.find_all('div',attrs={'class':'threadlist_abs'})[0].text)
        print('-{0}------------------------------------------------'.format(count))
        count += 1
