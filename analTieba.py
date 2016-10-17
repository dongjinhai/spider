import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pymysql.cursors
import time
import datetime
'''
分析贴吧发帖
- 记录贴吧的新帖增长速率
    1.判断一个帖子是不是新帖：如果帖子发表时间
      是和当前时间相差在30秒之内就判为新帖。
      但是由于帖子的发表时间不在静态页面上，所以使用selenium+phantomJS,
      速度有点慢。
    各位老司机们有没有更好的方法？
'''
# 得到当前时间，格式为xxxx-xx-xx xx:xx:xx
def getTimeNow():
    timeFormat = '%Y-%m-%d %X'
    return time.strftime(timeFormat,time.localtime())

# 将时间转化成datetime类型
def strTodatetime1(str):
    return datetime.datetime.strptime(str,'%Y-%m-%d %H:%M:%S')

def strTodatetime2(str):
    return datetime.datetime.strptime(str,'%Y-%m-%d %H:%M')

# 连接mysql数据库，返回一个数据库连接对象
def getMySqlCon():
    con = pymysql.connect(
        host = 'localhost',
        user = 'root',
        password = '25000',
        db = 'tieba',
        charset='utf8mb4',
        cursorclass = pymysql.cursors.DictCursor)
    return con
# 得到源html代码。
def gethtml(url):
    retu = requests.post(url)
    return retu.content.decode('utf-8')
# 处理源代码
def getSoup(html):
    soup = BeautifulSoup(html,'lxml')
    # list_ul = soup.find_all('ul',attrs={'id':'thread_list','class':'threadlist_bright j_threadlist_bright'})
    return soup

# 得到贴吧帖子数和关注数，写入数据库
def savMennumAndInfornum(url):
    timeNow = getTimeNow()
    html = gethtml(url)
    soup = getSoup(html)
    inforList = []
    inforList.append(soup.find_all('title')[0].text)
    inforList.append(soup.find_all('span',attrs={'class':'card_menNum'})[0].text)
    inforList.append(soup.find_all('span',attrs={'class':'card_infoNum'})[0].text)
    inforList.append(timeNow)
    inforList[0] = "".join(inforList[0].split())
    # 写入数据库
    con = getMySqlCon()
    value = " values('{0}','{1}','{2}','{3}');".format(inforList[0],inforList[1],inforList[2],inforList[3])
    insert_sql = "insert into tieba(tieba_name,card_menNum,card_infoNum,time)"+value
    try:
        with con.cursor() as cur:
            cur.execute(insert_sql)
            con.commit()
    finally:
        cur.close()
        con.close()
    return inforList

# 得到首页上帖子信息，包括帖子url，发布时间，帖子得到第一个的回复时间。
def getInfo_tiezi(url):
    html = gethtml(url)
    soup = getSoup(html)
    list_ul = soup.find_all('ul',attrs={'id':'thread_list','class':'threadlist_bright j_threadlist_bright'})
    info_tiezi_list = []
    reg = re.compile(r'\d{4}\-\d{1,2}-\d{2} \d{2}:\d{2}')
    for i in list_ul:
        for j in i.find_all('li',attrs={'class':' j_thread_list clearfix'}):
            tiezi_url = j.find_all('a',attrs={'class':'j_th_tit'})[0].get('href')
            tiezi_html =  gethtml('http://tieba.baidu.com'+tiezi_url)
            # tiezi_soup = BeautifulSoup(tiezi_html,'lxml')
            tie_create_time = reg.findall(tiezi_html)
            temp_list = []
            temp_list.append(tiezi_url)
            if len(tie_create_time)>1:
                temp_list.append(tie_create_time[0])
                temp_list.append(tie_create_time[1])
            else:
                temp_list.append(tie_create_time[0])
                temp_list.append('')
            info_tiezi_list.append(temp_list)
    # 写入数据库
    con = getMySqlCon()
    try:
        for i in info_tiezi_list:
            value = " values('{0}','{1}','{2}');".format(i[0],i[1],i[2])
            insert_sql = "insert into tiezi(tiezi_url,tiezi_setime,tiezi_fitime)"+value
            with con.cursor() as cur:
                cur.execute(insert_sql)
                con.commit()
                cur.close()
    finally:
        con.close()
    return info_tiezi_list

# 分析贴吧每个时段关注人数和帖子增长率
def analNumfortieba():
    result_dict =[]
    #得到数据库数据
    con = getMySqlCon()
    try:
        with con.cursor() as cur:
            select_sql = "select DISTINCT * from tieba where tieba_name = 'bilibili吧_百度贴吧';"
            cur.execute(select_sql)
            result_set = cur.fetchall()
    finally:
        cur.close()
        con.close()
    #处理数据
    for i in range(len(result_set)-1):
        temp_dict = {}
        start = strTodatetime1(result_set[i]['time'])
        end = strTodatetime1(result_set[i+1]['time'])
        time = start+(end - start)/2
        temp_dict['time'] = time
        menNum = int("".join(result_set[i]['card_menNum'].split(',')))-int("".join(result_set[i+1]['card_menNum'].split(',')))
        infoNum = int("".join(result_set[i]['card_infoNum'].split(',')))-int("".join(result_set[i+1]['card_infoNum'].split(',')))
        temp_dict['card_menNumRate'] = menNum/(end-start).seconds
        temp_dict['card_infoNumRate'] = infoNum/(end-start).seconds
        result_dict.append(temp_dict)
    #显示数据
    for i in result_dict:
        print('时段：{0}帖子增长率：{1}人数增长率：{2}'.format(i['time'],i['card_infoNumRate'],i['card_menNumRate']))
    return result_dict

# 分析帖子第一个回复时间区间图
def analFirstreply():
    #得到数据库数据
    con = getMySqlCon()
    try:
        with con.cursor() as cur:
            select_sql = "select DISTINCT tiezi_url,tiezi_setime,tiezi_fitime from tiezi;"
            cur.execute(select_sql)
            result_set = cur.fetchall()
    finally:
        cur.close()
        con.close()
    #处理数据
    temp = 1
    # 在一分钟之内回复数
    leastOnemin = 0
    # 在1-3分钟之内回复数
    betweenOneandThree = 0
    # 在3-5分钟之内回复数
    betweenThreeandFive = 0
    # 在5分钟以上回复数
    aboveFive = 0
    # 未得到回复的帖子数
    noneReply = 0
    for i in result_set:
        # print(temp,end=' ')
        if i['tiezi_fitime'] == '':
            noneReply += 1
        else:
            setime = strTodatetime2(i['tiezi_setime'])
            fitime = strTodatetime2(i['tiezi_fitime'])
            flag = (fitime-setime).seconds
            if flag < 60:
                leastOnemin += 1
            elif flag>=60 and flag<180:
                betweenOneandThree += 1
            elif flag>=180 and flag<300:
                betweenThreeandFive += 1
            else:
                aboveFive += 1
    print('在一分钟之内回复数:{0}'.format(leastOnemin))
    print('在1-3分钟之内回复数:{0}'.format(betweenOneandThree))
    print('在3-5分钟之内回复数:{0}'.format(betweenThreeandFive))
    print('在5分钟以上回复数:{0}'.format(aboveFive))
    print('未得到回复的帖子数:{0}'.format(noneReply))





url='http://tieba.baidu.com/f?kw=bilibili&fr=index&fp=0&ie=utf-8'
'''
while True:
    re_list = savMennumAndInfornum(url)
    print(re_list)
    time.sleep(20)
'''
getInfo_tiezi(url)
analFirstreply()
'''
for i in getInfo_tiezi(url):
    print(i)
'''
# html = gethtml(url)
# soup = getSoup(html)
# print('关注数:'+soup.find_all('span',attrs={'class':'card_menNum'})[0].text)
# print('帖子数:'+soup.find_all('span',attrs={'class':'card_infoNum'})[0].text)
# list_ul = soup.find_all('ul',attrs={'id':'thread_list','class':'threadlist_bright j_threadlist_bright'})
# tie_list = []
# count = 0
# reg = re.compile(r'\d{4}\-\d{1,2}-\d{2} \d{2}:\d{2}')
# for i in list_ul:
#     for j in i.find_all('li',attrs={'class':' j_thread_list clearfix'}):
#         info_list = []
#         info_list.append(j.find_all('span',attrs={'title':'回复'})[0].text)
#         info_list.append(j.find_all('a',attrs={'class':'j_th_tit'})[0].text)
#         info_list.append(j.find_all('a',attrs={'class':'j_th_tit'})[0].get('href'))
#         info_list.append(j.find_all('span',attrs={'class':'frs-author-name-wrap'})[0].text)
#         info_list.append(j.find_all('span',attrs={'class':'pull-right'})[0].text)
#         info_list.append(j.find_all('div',attrs={'class':'threadlist_abs'})[0].text)
#         print('-{0}------------------------------------------------'.format(count))
#         # html = gethtml('http://tieba.baidu.com'+info_list[2])
#         '''# 这段代码用来抓每个帖子的发布时间，但是由于采用了Phantomjs，导致比较慢
#         driver = webdriver.PhantomJS(executable_path=r'E:\workplace\phantomjs-2.1.1-windows\bin\phantomjs.exe')
#         driver.get('http://tieba.baidu.com'+info_list[2])
#         html = driver.page_source
#         soup = BeautifulSoup(html,'lxml')
#         print(str(soup))
#         tie_create_time = reg.findall(str(soup))
#         info_list.append(tie_create_time)
#         '''
#         count += 1
#         tie_list.append(info_list)
#         break
#     break
#
# for i in tie_list:
#     print(i)