import os
import re
import requests
from bs4 import BeautifulSoup
# open('E:\\xiaoshuo\\text.txt','w')
'''
reg = re.compile(r'[/\:*?<>"|]+')
print(type(reg))
testStr = '第六十八章 你是怎么逃出来的?'
re_list = reg.findall(testStr)
print(re_list)
testStr = testStr.replace(re_list[0],'')
print(testStr)
'''
with open('E:\\xiaoshuo\\test.html','w') as f:
    f.write(r'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Title</title></head><body background="green">')
    f.write('1141343<br>')
    f.write(r'</body></html>')
'''
url = 'http://www.biquku.com/3/3226/2021814.html'
retu = requests.get(url)
soup = BeautifulSoup(retu.content.decode('gbk',errors='ignore'),'lxml')
con_list = soup.find_all('div',attrs={'id':'content'})
print(con_list[0])
'''