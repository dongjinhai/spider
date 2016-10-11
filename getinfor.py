import requests
from bs4 import BeautifulSoup
def getsource(url):
    header = {
        'Host':'jwxt.xtu.edu.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Cookie':'JSESSIONID=5EA538778B8C2D34830B20BA2471FE17',
    }
    retu = requests.post(url,headers=header)
    return retu.content.decode('utf-8',errors = 'ignore')

def chuli(html):
    soup = BeautifulSoup(html)
    return soup.prettify()


url = 'http://jwxt.xtu.edu.cn/jsxsd/kscj/cjcx_list?xq=null'
retu = getsource(url)
print(retu)