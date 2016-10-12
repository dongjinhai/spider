import re

'''
重写格式对其函数。
'''
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

# for i in xila:
#     print(myAlign(i,4),end=' ')