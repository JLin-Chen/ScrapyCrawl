本文档用于记录USWOO爬取StreetEasy网站上不同地区不同房型的最低价信息并整合成一个csv表格的项目。因所有代码均根据个人目前的学习与理解整理而得，
可能某些代码存在错误或者并不是最优选择，后续也将根据学习的深入和进展进行一定的补充和优化。

# dataset

link_info: 用于记录爬取数据的网站以及所需的Xpath信息。其中，A-大楼名称，B-大楼网站链接，C-大楼单元名称，D-房间beds，E-房间baths，F-出租价格

# main

因为不同大楼的链接不能通过数据爬取获得，所以在building_list中按照各个大楼的信息进行人工搜索，并且记录不同页面不同结构的Xpath，最后整合成link_info.csv文件，用于
在spider.py文件中导入待爬取页面的信息。

任务总共分为两个部分：

第一部分，首先先根据link_info中的信息获取对应大楼的所有available房型信息输出至house_info.csv，然后对获取到的数据进行数据清洗data_clean.py，保存至house_info_clean.csv，经过筛选，输出大楼中不同户型的最低价房源信息至house_info_pricemin.csv。

第二部分，根据house_info_pricemin.csv中的低价房源信息，查看低价户型中是否还有优惠价，即到相应子页面中爬取是否存在Free Month相关内容。

__第一部分:__

因为我们是从csv文件中读取结构化的数据，所以选择用pandas进行导入（当然也可以用其他方法没有必要一定动用dataframe）：

```python
 allowed_domains = ["streeteasy.com"]
 df = pd.read_csv('link_info.csv', encoding='utf-8')
 ```
 最终需要对不同的大楼url进行爬取，所以我们采用列表的形式存入所有需要爬取的url信息：
 
 ```python
 start_urls = []
    building_name = []
    xpath_unit = []
    xpath_beds = []
    xpath_baths = []
    xpath_price = []
    length = len(df)
    for i in range(length):
        start_urls.append(df['link'][i])
        building_name.append(df['building_name'][i])
        xpath_unit.append(df['unit'][i])
        xpath_beds.append(df['beds'][i])
        xpath_baths.append(df['baths'][i])
        xpath_price.append(df['price'][i])
      ```
上述的列表信息将会在下文提到的函数中用到，这里涉及到了一个内部调用问题。因为列表的下标是从[0]开始，所以初始化num_url=-1，以便控制
后续的爬取工作是对同一行相应url的xpath展开的，防止不同行之间的串扰。（这也需要控制爬虫程序禁止并发，否则会造成错误，这个坑也是搞了很久求助某位大佬才跳出来）

与lianjia项目中爬取单个url不同，因为涉及到对多个url进行爬取操作，我们需要定义一个start_request()来告知爬虫项目当前对哪个url进行爬取：

```python

    def start_requests(self):
        for url in self.start_urls:
            sleeptime = random.randint(0, 10)
            time.sleep(sleeptime)
            cookie=''
            Cookie = {'Cookie':cookie}
            yield scrapy.Request(url=url,cookies=Cookie,callback=self.parse)
```

其中，我们设置的timesleep和cookie都是为了绕过反爬机制，在运行该项目时，测试代码和试爬取都是成功的，但可能因为爬取的次数过多，后续项目的开展在反爬这一块受阻，
下一步的研究将针对如何反爬以及设置IP代理池展开，解决方案或许会再更新。

获取url信息的步骤我们在parse()中定义：

```python
    def parse(self, response):
        item = Test1Item()
        self.num_url = self.num_url + 1

        for n in range(5):
            item['building_name'] = self.building_name[self.num_url]
            item['unit'] = response.xpath((self.xpath_unit[self.num_url]+'/text()').format(n+1)).extract()
            item['beds'] = response.xpath(self.xpath_beds[self.num_url].format(n+1)).extract()
            item['baths'] = response.xpath(self.xpath_baths[self.num_url].format(n+1)).extract()
            item['price'] = response.xpath(self.xpath_price[self.num_url].format(n+1)).extract()
            item['url_py'] = response.xpath((self.xpath_unit[self.num_url]+'/@href').format(n+1)).extract()
            # print(item['url_py'])
            if item['building_name'and'unit'and'beds'and'baths'and'price']:
                yield item
```

有几点需要注明的是，获得到的url_py是用于存储对应房型具体信息的跳转链接（部分链接存在不完整情况，在data_clean.py中进行数据清洗时补充完整）。
以上是完成第一部分爬取原网页信息的内容。接下来我们要进行第二部分跳转网页信息的爬取。

__第二部分：__

其实，第二部分的代码与第一部分并没有很大的差别，是在第一部分的基础上稍加改动得到的，我们只需要根据获取的信息的不同，在第一部分代码的初上，
修改相应的Xpath信息即可。

```python
 def parse(self, response):
         item = Test1Item()
         self.num_url = self.num_url + 1
         
         item['building_name'] = self.building_name[self.num_url]
         item['unit'] = self.xpath_unit[self.num_url]
         item['beds'] = self.xpath_beds[self.num_url]
         item['baths'] = self.xpath_baths[self.num_url]
         item['price'] = self.xpath_price[self.num_url]
         item['price_min'] = response.xpath('//*[@id="content"]/main/div[3]/article[2]/section[1]/div/div[2]/ul/li[1]/p/text()').extract()
         print(item['building_name'])
         print(item['price_min'])
         # if item['building_name'and'unit'and'beds'and'baths'and'price']:
         #
         #     yield item
```






