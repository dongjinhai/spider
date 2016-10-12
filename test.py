import os
import re
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
    f.write('1141343<br>')
    f.write('dahdoa')