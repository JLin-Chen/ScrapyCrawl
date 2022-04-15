import csv
import pandas as pd
import time
import pandas
import re

# 打开CSV文件，载入数据
fileNameStr = 'house_info.csv'
df = pd.read_csv(fileNameStr, encoding='utf-8')

# 进行数据清洗,并输出至文件
fp = open("house_info_clean.csv", 'w', newline="", errors="ignore", encoding='utf-8')
writer = csv.writer(fp)
head = ['building_name','unit','beds','baths','price','url_py_add']
writer.writerow(head)
for i in range(len(df)):
    building_name=''
    unit=''
    beds=''
    baths=''
    price=''
    url_py=''
    url_py_add=''
    building_name=df['building_name'][i]
    unit = df['unit'][i].replace('[','').replace(']','').replace("'",'')
    beds = df['beds'][i].replace(' ','').replace("'",'').replace("\\n",'').replace(',','').replace('[','').replace(']','')
    baths = df['baths'][i].replace(' ', '').replace("'", '').replace("\\n", '').replace(',', '').replace('[','').replace(']','')
    price = df['price'][i].replace(' ', '').replace("'", '').replace("\\n", '').replace(',', '').replace('$','').replace('[','').replace(']','')
    url_py = df['url_py'][i].replace('[','').replace(']','').replace("'",'')
    # print(beds,baths,price)
    flag=0
    for ch in url_py:
        if ch=='h':
            flag=1
            break
        if ch=='/':
            flag=2
            break
    if flag==1:
        url_py_add=url_py
    if flag==2:
        url_py_add='https://streeteasy.com'+url_py
    a = [building_name,unit,beds,baths,price,url_py_add]
    writer.writerow(a)
fp.close()

# 计算不同大楼不同户型的最低价，输出筛选后的数据到文件
fileNameStr = 'house_info_clean.csv'
df = pd.read_csv(fileNameStr, encoding='utf-8')

s = df['price'].groupby([df['building_name'], df['beds'],df['baths']]).min()
s.to_csv("house_info_pricemin.csv", mode='w', header='building_name''beds''baths''price_min')
