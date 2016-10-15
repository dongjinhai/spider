import requests
from bs4 import BeautifulSoup
# from spider.myAlign import myAlign
def getsource(url):
    xq = input('请输入学期：格式xxxx-xxxx-x:')
    params = {
        'xq':xq,
              }
    header = {
        'Host':'jwxt.xtu.edu.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Cookie':'JSESSIONID=4EC0D2D7AC66EF00315D37AD9FC5B65D',
    }
    retu = requests.post(url,headers=header,params=params)
    return retu.content.decode('utf-8',errors = 'ignore')

def chuli(html):
    soup = BeautifulSoup(html,'lxml')
    for tr in soup.find_all('tr'):
        for td in tr.find_all('td'):
            print(td.text,end=' ')
        print()
    # return soup.prettify()


url = 'http://jwxt.xtu.edu.cn/jsxsd/kscj/cjcx_list'
retu = getsource(url)
chuli(retu)
# print(retu)