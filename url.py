import urllib.request
import re
# 返回一个response对象。
set_headers={
    'Host':'jwxt.xtu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Cookie':'JSESSIONID=5256B08307D3AE747D21AF4C29AC67AC',
}
request = urllib.request.Request('http://jwxt.xtu.edu.cn/jsxsd/kscj/cjcx_list?xq=null',headers=set_headers)
response = urllib.request.urlopen(request)
back = response.read().decode('utf-8',errors='ignore')
res_list = re.findall(r"<tr>(.*?)</tr>",back,re.S)
# print(back)
for i in res_list:
    result = re.findall(r'<th.*?>(.*?)</th>',i)
    if len(result) is 0:
        result = re.findall(r'<td.*?>(.*?)</td>',i)
    print(result)