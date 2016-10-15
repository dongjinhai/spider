import pymysql.cursors

con = pymysql.connect(host='localhost',
                      user='root',
                      password='25000',
                      db='gzc',
                      charset='utf8mb4',
                      cursorclass=pymysql.cursors.DictCursor)
select_sql = "select * from news where types <= 5"
try:
    with con.cursor() as cur:
        cur.execute(select_sql, )
        result = []
        result = cur.fetchall()
        for elms in result:
            print(elms)
finally:
    con.close()

# import pymysql
# conn = pymysql.connect(host='localhost', port=3306,user='root',passwd='root',db='DeliveryAddress',charset='UTF8')
# cur = conn.cursor()
# cur.execute("INSERT INTO `ProvinceCityCountyTown` VALUES ('3', '0', '上海')")
# conn.commit()#这里是用conn提交的,很让人不解，为什么不用cur提交呢？害得我baidu都没找到例子，
# cur.close()
# conn.close()