import requests
from bs4 import BeautifulSoup
import time
import re
'''
爬取遮天的小说，下载下来
'''
def getHerfAndTitle(url):
    all_list = []
    retu = requests.get(url)
    soup = BeautifulSoup(retu.content,'lxml')
    for i in soup.find_all('dd'):
        child_list = []
        child_list.append(i.find_all('a')[0].text)
        child_list.append(i.find_all('a')[0]['href'])
        all_list.append(child_list)
    return all_list

def getContent(all_list):
    reg = re.compile(r'[/\:*?<>"|]+')
    time_count = 0
    for i in all_list:
        #防止爬太快而被主机拒绝
        if time_count >= 50:
            time.sleep(1)
            time_count=0
        time_count += 1
        url = 'http://www.biquku.com/3/3226/'+i[1]
        retu = requests.get(url)
        soup = BeautifulSoup(retu.content.decode('gbk',errors='ignore'),'lxml')
        con_list = soup.find_all('div',attrs={'id':'content'})
        # 文件名可能含有非法字符，不能创建，需要剔除非法字符
        re_list = reg.findall(i[0])
        for item in re_list:
            i[0] = i[0].replace(item,'')
        with open('E:\\xiaoshuo\\{0}.html'.format(i[0]),'w') as f:
            f.write(r'<!DOCTYPE html><html lang="en"><head><meta charset="GBK"><title>Title</title></head><body bgcolor="#deb887">')
            f.write(str(con_list[0]).encode('GBK','ignore').decode('GBK',errors='ignore'))
            f.write(r'</body></html>')
        print(i)

url = 'http://www.biquku.com/3/3226/index.html'
all_list = getHerfAndTitle(url)
getContent(all_list)

# for i in all_list:
#     print(i)
