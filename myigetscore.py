from selenium import webdriver
import time

driver = webdriver.PhantomJS(executable_path=r'E:\workplace\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver.get('http://202.197.224.134:8083/jwgl/login.jsp')

# print(driver.page_source)
print('>>>查询成绩开始....')
print('>>>开始登录教务管理系统...')

# 登录教务管理系统
driver.find_element_by_name('username').send_keys('2013552026')
driver.find_element_by_name('password').send_keys('107658')
driver.find_element_by_tag_name('form').submit()

print('>>>登录成功！')
# 进入frame标签，并选择点击‘成绩管理’
frameElement = driver.find_elements_by_tag_name('frame')
driver.switch_to_frame(frame_reference=frameElement[0])
# driver.find_element_by_link_text(link_text="messeges.jsp")
alist = driver.find_elements_by_tag_name('a')
# driver.find_element_by_tag_name('title')
alist[3].click()
# 延时是必须的，不然会出现“Element is no longer attached to the DOM”错误
time.sleep(1)

print('>>>选择成绩管理...')
# 出现成绩查询的<a>标签后然后点击
aerlist = driver.find_elements_by_tag_name('a')
# for i in aerlist:
#     print(i.text)
aerlist[4].click()
time.sleep(1)

# print(driver.page_source)

# 转到第三个frame
# print('------------------第三个frame----------------')
driver.switch_to_default_content()
driver.switch_to_frame(frame_reference=frameElement[2])

# 对下拉框进行操作
# print(driver.page_source)
print('>>>选择查询所有学期...')
drop_down = driver.find_element_by_name('xq')
drop_down.find_element_by_xpath("//option[@value='0']").click()
time.sleep(1)
driver.find_element_by_xpath("//input[@value='查询成绩']").click()
time.sleep(1)

# print(driver.page_source)

finalScore = driver.find_elements_by_tag_name('tr')
print('>>>成功get，开始返回...')

# 重写格式对其函数
import re
temp = re.compile(u'[\u4e00-\u9fa5]+')
xila = ['Ⅰ','Ⅱ','Ⅲ','Ⅳ','Ⅴ','Ⅵ','Ⅶ','Ⅷ']
def myAlign(istr,length=0):
    if length is 0:
        return istr
    strlen = len(istr)
    re = istr
    i = 0
    count = 0
    placeholder = ' '
    while i < strlen:
        if temp.match(istr[i]):
            count += 2
            # placeholder =u'　'
        elif istr[i] in xila:
            count += 2
        else:
            count += 1
            # placeholder = ' '
        i += 1
    while count < length:
        re += placeholder
        count += 1
    return re

for e in finalScore:
    for i in e.find_elements_by_tag_name('td'):
        print(myAlign(i.text,30),end='')
    print('')


print('>>>返回成功！')
driver.quit()
print('>>>退出程序成功！')
