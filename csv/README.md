# 涉及csv、json、pandas的操作指南

该文档用于记录爬虫项目中常用的csv数据清洗以及数据整理操作，用于进一步分析爬获取的文件。

---

## 1.用pandas打开csv文件读取数据信息

```python
import pandas

# 1.打开CSV文件
fileNameStr = 'filename.csv'
df = pd.read_csv(fileNameStr, encoding='utf-8', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9])

print("============= head ===================")
print(df.head())
print("============= describe ===============")
print(df.describe())
print("============= info ===================")
print(df.info())

# 2.查看是否有缺失值
print("============== 缺失值情况 ========================")
print(df.isnull().sum().sort_values(ascending=False))
print("==================================================")

```
## 2. csv的简单数据计算

```python
# 1.去掉四列data数据全部为空的行，并写入文件
print(df.info())
df.dropna(axis='index', how='all',
          subset=['data1', 'data2', 'data3', 'data4'], inplace=True)
print("**********************************")
print(df.info())
df.to_csv("output.csv")

# 2.计算每一行的平均值
df['sum'] = df[['data1', 'data2', 'data3', 'data4']].sum(axis=1) # axis=0列，axis=1行
df['count'] = df[['data1', 'data2', 'data3', 'data4']].count(axis=1)
df['ave'] = round(df['sum']/df['count'], 2)

# 3.输出到文件
df.to_csv("output.csv")

# 4. 汇总计算PM指数年平均值的变化情况
s1 = df['ave'].groupby(df['year']).mean()
print(s1)
s1.to_csv("PM_Beijing.csv", mode='a', header='year''average')

# 5. 按年分组，计算每年中1-12月份的PM指数数据变化情况
s2 = df['ave'].groupby([df['year'], df['month']]).mean()
print(s2)
s2.to_csv("PM_Beijing.csv", mode='a', header='year''month''average')

```

## 3. DataFrame相关操作

```python

import pandas as pd

# 读取csv
pd.read_csv('filename.csv')

# 存储为csv文件
submission = pd.DataFrame({'PassengerID': df['PassengerID'], 'Survived': predictions})
submission.to_csv("submission.csv", index=False)  # index参数是否写入行names键

# 从dict生成
pd.DataFrame.from_dict(df, orient='index')
pd.DataFrame({'a': [1, 2], 'b': [2, 3]}, columns=['a', 'b'])  # a,b分别为列
pd.DataFrame.from_dict({'a': [1, 2], 'b': [2, 3]}, orient='index')  # a,b分别为行

# 选择数据
df['']  # 通过键选择列
df[['A', 'B']]  # 通过list选择列
df[0:3]  # 通过隐含的序列（index所在行值）选择行
df['20130102':'20130104']  # 通过行index键选择行

```

## 4. csv获取/删除特定内容

获取特定内容：

```python
import pandas as pd
import csv
import os

def save_to_csv(file_name_number):
    df = pd.read_csv(path + '\\{}.csv'.format(file_name_number), encoding='gbk', usecols=[0, 1])
    fp = open("Weibo_comment2.csv", 'a+', newline="", errors="ignore", encoding='gbk')
    writer = csv.writer(fp)
    b = str(df['text'][1])
    o = 1
    for i, row in df.iterrows():

        flag = 0
        if '转发微博' in str(df['text'][i]):
            flag = 1
        if '转发微博。' in str(df['text'][i]):
            flag = 1
        if '轉發微博' in str(df['text'][i]):
            flag = 1
        if o > 10:
            break
        if i >= 2 and flag == 0:
            b = b + '\t' + str(df['text'][i])
            o += 1

    c = str(df['text'][1]) + '\t' + str(df['text'][2])
    a = [df['id'][0], df['text'][0], c, b]
    writer.writerow(a)
    a = []
    b = ''
    c = ''
    fp.close()


no_1_file = ".DS_Store"
path = r'0720\Weibo_json_to_csv'
k = 0
lis = os.listdir(path)
for li in lis:
    file_name = []
    if "csv" in li:
        li = li.replace('.csv', '')
        file_name.append(li)
        file_name_number = ''.join(file_name)
        save_to_csv(file_name_number)
        file_name = []
        k += 1
        continue
    if li in no_1_file:
        continue

print('Finished. 总共处理', k, '个csv文件')

```

删除指定内容：

```python
OUTPUT = 'output.csv'
EXCLUDE_KEYWORDS = ['股票', '数字V.X', 'sz', 'sh']

data = dict()
filenames = os.listdir('20190415')
for filename in filenames:
    with open(os.path.join('20190415', filename), 'r', encoding='UTF-8') as f:
        contents = re.findall(r'<CONTENT>(.*?)</CONTENT>', f.read())  # 正则匹配
        for content in contents:
            # 剔除含指定关键词
            for exclude_keyword in EXCLUDE_KEYWORDS:
                if exclude_keyword in content:
                    break
            # 不含则存入data
            else:
                if content not in data:
                    data[content] = {'filenames': [filename], 'count': 1}
                else:
                    data[content]['filenames'].append(filename)
                    data[content]['count'] += 1
        f.close()
# 写入文件
with open(OUTPUT, 'w', encoding='utf-8-sig') as f_output:
    f_output.write('"content","filenames","count"\n')
    for each in data:
        f_output.write('"{}","{}",{}\n'.format(each, data[each]['filenames'], data[each]['count']))
f_output.close()
```

## 5. 给csv中的特定内容添加标签后写入txt

```python
import pandas as pd


df = pd.read_csv('Weibo_id&text(1)(1).csv', encoding='unicode_escape', usecols=[0, 4, 5, 6])
fi = open('Weibo.txt', 'r', encoding='utf-8')

i = 0
for line in fi:
    temp1 = line.strip('\n')
    temp2 = temp1.split(' ')
    eid = ''
    label = ''
    flag = 0
    for ch in temp2[0]:
        if ch == 'a':
            flag = 1
        if flag == 1 and ch == '\t':
            break
        if flag == 0:
            if ch in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                eid += ch
        if flag == 1:
            if ch in ('0', '1'):
                label = ch
    # print(type(eid))
    # if int(eid) == int(df['id'][i]):
    if label == '1':
        df['fake_label'][i] = 1
        df['real_label'][i] = 0
    if label == '0':
        df['fake_label'][i] = 0
        df['real_label'][i] = 1
    df['ncw_label'][i] = label
    i += 1
    if i == 4663:
        break
print(i)
df.to_csv('Weibo_id&text(1).csv')
```

## 6. csv中的大数值型数据转换为str

```python
df['id'] = str(file_name_number) + '\t' # 防止csv中数字用科学计数法表示
```

## 7. 读取某键值的第一个元素

```python
writer = csv.writer(fp)
a = [df['text'][0],df['test'][0]]
writer.writerow(a)
```
## 8. json to csv的相关操作

将json中的所有数据导入csv：

```python
import json
import csv

file_in = open('4010312877.json', 'r', encoding='utf-8')
data_str = file_in.read()

# print("字符串头：", data_str[:100])
# print("字符串尾：", data_str[-100:])

data_str = data_str.replace('true', 'True')
data_str = data_str.replace('false', 'False')
data_str = data_str.replace('null', 'None')
data_str = data_str.replace('\n', '')
# data_str = data_str.replace('[', '')
# data_str = data_str.replace(']', '')


def query_type(data):
    for ch in data:
        if ch == '{':
            return "dict"
        if ch == '[':
            return "list"
    return "value"


data_head = []


def get_json_head(data, loc=""):
    # data = str(data)
    print(data)
    data_type = query_type(data)
    if data_type == "value":
        if loc[1:] not in data_head:
            data_head.append(loc[1:])
        return
    if data_type == "dict":
        data_dict = eval(data)
        for keys in data_dict:
            get_json_head(data_dict[keys], loc + "_" + keys)
        return
    if data_type == "list":
        data_list = list(eval(data))
        for item in data_list:
            get_json_head(item, loc)
        return


get_json_head(data_str)

print(data_head[:10])
print(data_head[-10:])
print("表头数量：", len(data_head))

data_head_dict = {}
for head in data_head:
    tmp = []
    for i in range(200):
        tmp.append("")
    data_head_dict[head] = tmp
for key in data_head[:10]:
    print(key, data_head_dict[key][:10], len(data_head_dict[key]))
    pass

row_now = 0


def get_json_table(data, loc="", rows=0):
    global row_now
    # data = str(data)
    data_type = query_type(data)
    if data_type == "value":
        key = loc[1:]
        data_head_dict[key][rows] = data
        return

    if data_type == "list":
        data_list = list(eval(data))
        for i in range(len(data_list)):
            if i > 0:
                row_now += 1
            get_json_table(data_list[i], loc, row_now)
        return


get_json_table(data_str)
for key in data_head[:10]:
    print(key, data_head_dict[key][:10], len(data_head_dict[key]))
    pass

file_out = open('4010312877.csv', 'w', encoding='gbk')
for head in data_head[:-1]:
    file_out.write(head)
    file_out.write(",")
file_out.write(data_head[-1] + "\n")
for i in range(200):
    for head in data_head[:-1]:
        file_out.write(data_head_dict[head][i])
        file_out.write(",")
    last_key = data_head[-1]
    file_out.write(data_head_dict[last_key][i])
    file_out.write("\n")
```

获取json中的特定内容写入csv：

```python
import json
import csv
import os


def save_to_csv(file_name_number):
    f = open(path + '\\{}.json'.format(file_name_number), 'r', encoding='utf-8')
    content = f.read()
    data = json.loads(content)
    fp = open(r'E:\UIR\课题-谣言监测\0720\Weibo_json_to_csv' + '\\{}.csv'.format(file_name_number), 'w', newline="", errors="ignore", encoding='gbk')
    writer = csv.writer(fp)
    writer.writerow(['id', 'text', 'Followers_count', 'Statues_count', 'Friends_count'])
    for i in data:
        row = [str(i['id']), i['text'], str(i['followers_count']), str(i['statuses_count']), str(i['friends_count'])]
        writer.writerow(row)
    f.close()


no_1_file = ".DS_Store"
path = r'E:\UIR\课题-谣言监测\0720\Weibo'
count = 0
lis = os.listdir(path)
for li in lis:
    file_name = []
    if "json" in li:
        # file_name.append(os.path.join(path, li))
        li = li.replace('.json', '')
        file_name.append(li)
        file_name_number = ''.join(file_name)
        # print(file_name_number)
        save_to_csv(file_name_number)
        file_name = []
        count += 1
        continue
    if li in no_1_file:
        continue
print('转换完成,共计', count, '条信息')
```

获取json文件中特定字符后的内容写入csv：

```python
import json
import csv
import os


def save_to_csv(file_name_number):
    f = open(path + '\\{}.json'.format(file_name_number), 'r', encoding='utf-8')
    content = f.read()
    data = json.loads(content)

    fp = open(r'E:\UIR\课题-谣言监测\0720\Weibo@_json_to_csv' + '\\{}.csv'.format(file_name_number), 'w', newline="", errors="ignore", encoding='gbk')
    writer = csv.writer(fp)
    writer.writerow(['id', 'text', 'Followers_count', 'Statues_count', 'Friends_count'])
    flag = 0
    for i in data:
        text = i['text']
        for ch in text:
            if ch == '@':
                row = [str(i['id']), i['text'], str(i['followers_count']), str(i['statuses_count']),
                       str(i['friends_count'])]
                print(text)
                flag = 1
                writer.writerow(row)
                break
    if flag == 0:
        fp.close()
        os.remove(r'E:\UIR\课题-谣言监测\0720\Weibo@_json_to_csv' + '\\{}.csv'.format(file_name_number))
    f.close()


no_1_file = ".DS_Store"
path = r'E:\UIR\课题-谣言监测\0720\Weibo'
count = 0
lis = os.listdir(path)
for li in lis:
    file_name = []
    if "json" in li:
        # file_name.append(os.path.join(path, li))
        li = li.replace('.json', '')
        file_name.append(li)
        file_name_number = ''.join(file_name)
        # print(file_name_number)
        save_to_csv(file_name_number)
        file_name = []
        count += 1
        continue
    if li in no_1_file:
        continue
print('转换完成,共处理', count, '个json文件')
···

## 9.读入多个文件夹中的json文件

```python
# -*- coding:utf-8 -*-
import json,re,os,csv

no_1_file = ".DS_Store"
yes_file = "source-tweet"
path = r'D:\5pheme-rnr-dataset\5pheme-rnr-dataset'
file_name = []
name = ['文件名','text','id','user_id']
# def save_csv()
charliehebdo = "charliehebdo"
ferguson = "ferguson"
germanwings_crash = "germanwings-crash"
ottawashooting = "ottawashooting"
sydneysiege = "sydneysiege"


def save_csv(file_name, title_name, content):
    if type(title_name) == list:
        title_name = tuple(title_name)
    elif type(title_name) == dict:
        title_name = tuple(title_name.values())
    if type(content) == list:
        content = tuple(content)
    elif type(content) == dict:
        content = tuple(content.values())
    with open("{}.csv".format(file_name), "a+", newline="", errors="ignore", encoding="gbk") as a:
        writer = csv.writer(a)
        # 以读的方式打开csv文件
        with open("{}.csv".format(file_name), "r", newline="", errors="ignore", encoding="gbk") as f:
            reader = csv.reader(f)
            # 判断是否有标题，如果没有则写入标题和内容，如果有则写入内容
            if not [row for row in reader]:
                writer.writerow(title_name)
                writer.writerow(content)
            else:
                writer.writerow(content)

def get_file(path):
    lis = os.listdir(path)
    for li in lis:
        if li == "reactions":
            continue
        if "json" in li and yes_file in path:
            file_name.append(os.path.join(path,li))
            continue
        if li in no_1_file:
            continue
        get_file(os.path.join(path,li))

def get_data(path):
    with open(path,'r')as f:
        data = json.load(f)
    text = data['text']
    id = str(data['id'])+"\t"
    use_id = str(data['user']['id'])+"\t"
    title = path.split('\\')[-1].replace(".json","")+"\t"
    if charliehebdo in path:
        save_csv(charliehebdo,name,[title,text,id,use_id])
    elif ferguson in path:
        save_csv(ferguson, name, [title, text, id, use_id])
    elif germanwings_crash in path:
        save_csv(germanwings_crash, name, [title, text, id, use_id])
    elif ottawashooting in path:
        save_csv(ottawashooting, name, [title, text, id, use_id])
    elif sydneysiege in path:
        save_csv(sydneysiege, name, [title, text, id, use_id])

if __name__ == '__main__':
    get_file(path)
    for file in file_name:
        get_data(file)
```


















