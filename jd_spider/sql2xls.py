# -*- coding: utf-8 -*-

# Convert from sql to excel book (.xls)

import xlwt
import MySQLdb

conn = MySQLdb.connect('localhost','root','','jingdong',charset='utf8')
cursor = conn.cursor()

count = cursor.execute('select product_id,comment_count,comment_version from jd_products')
# 重置游标的位置
cursor.scroll(0,mode='absolute')
# 搜取所有结果
results = cursor.fetchall()

# 获取MYSQL里面的数据字段名称
fields = cursor.description
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('table_goods',cell_overwrite_ok=True)

# 写上字段信息
# for field in range(0,len(fields)):
#     sheet.write(0,field,fields[field][0])

# 获取并写入数据段信息
row = 0
col = 0
for row in range(0,len(results)):
    for col in range(0,len(fields)):
    	# print str(row) + ' ' + str(col) + ' ' + str(results[row][col])
        sheet.write(row,col,u'%s'%results[row][col])

workbook.save(r'./goods.xls')
cursor.close()
conn.close()
print "Convert Succeed!"

