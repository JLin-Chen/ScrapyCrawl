# 初初初学者友好的指南

__1. begin.py__

整个爬虫项目从begin.py开始运行，该文件中通过调用系统命令行进行操作。其中，lianjia是爬虫的名字，需要与spider中的爬虫名字相同
才能正确调用。

```python

from scrapy import cmdline

cmdline.execute("scrapy crawl lianjia".split())

```

__2. spider.py__

文件中包含着爬虫项目的主题，爬取具体网页所需的内容均在此.py文件中编辑。

来看一个例子：

```python
import scrapy

from test.items import TestItem


class Test5Spider(scrapy.spiders.Spider):
    name = "lianjia"  # 注意与命令行调用的爬虫名字相同
    allowed_domains = ["bj.lianjia.com"]

    start_urls = [] # 开始爬取的网址
    for n in range(4):
        for m in range(4):
            url = "https://bj.lianjia.com/ershoufang/a[{}]/pg{}rs%E5%8C%97%E4%BA%AC/".format(n, m + 1)
            start_urls.append(url)
            def parse(self, response):
                item = Test5Item()
                for n in range(30):
                    item['name'] = response.xpath(
                        "/html/body/div[4]/div[1]/ul/li[{}]/div[1]/div[2]/div/a[1]/text()".format(n + 1)).extract()
                    item['location'] = response.xpath(
                        "/html/body/div[4]/div[1]/ul/li[{}]/div[1]/div[2]/div/a[2]/text()".format(n + 1)).extract()
                    item['houseinfo'] = response.xpath(
                        "/html/body/div[4]/div[1]/ul/li[{}]/div[1]/div[3]/div/text()".format(n + 1)).extract()
                    item['total_price'] = response.xpath(
                        "/html/body/div[4]/div[1]/ul/li[{}]/div[1]/div[6]/div[1]/span/text()".format(n + 1)).extract()
                    item['unit_price'] = response.xpath(
                        "/html/body/div[4]/div[1]/ul/li[{}]/div[1]/div[6]/div[2]/span/text()".format(n + 1)).extract()

                    if item['name' and 'location' and 'houseinfo' and 'total_price' and 'unit_price']:
                        yield item
```

__3. items.py__

该文件中用来定义文件需要爬取的内容，在items中定义的内容需要和pipelines.py以及spider.py中涉及items的内容保持一致，
否则会出现爬取不到具体内容的DeBUG(200)错误。

```python
import scrapy

class TestItem(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    houseinfo = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
```

__4. middlewares.py__

对于初级的爬虫，我们不需要去改变middleware中的内容，保持默认设置即可。

__5. pipelines.py__

pipeline用于定义爬取的内容的输出。

输出至csv文件：

```python
import csv

class Test5Pipeline(object):
    def __init__(self):
        self.fp = open('house_info.csv', 'w', encoding='gbk',newline='')
        self.headers = [
            'name', 'location', 'houseinfo',  'total_price', 'unit_price'
        ]
        self.writer = csv.DictWriter(self.fp, self.headers)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.ITEM = []
        self.ITEM.append(item)
        self.writer.writerows(self.ITEM)
        return item

    def close_spider(self,spider):
        self.fp.close()
```

输出至json文件：

```python
import json

class Test5Pipeline(object):
    def __init__(self):
        self.file = None

    def open_spider(self,spider):
        try:
            self.file = open("Test5Item.json", "w", encoding="utf-8")
        except Exception as err:
            print(err)

    def process_item(self, item, spider):
        dict_item = dict(item)
        json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"
        self.file.write(json_str)
        return item

    def close_spider(self, spider):
        self.file.close()
```

__6. settings.py__

该文件用于设置项目中的一些设置内容，当遇上反爬措施或是其他网站报错的话，需要更改setting中的一些设置。robot协议也在此中
进行修改。

```python
BOT_NAME = 'lianjia'  # 爬虫名字，注意与begin.py及spider.py中的name保持一致。
SPIDER_MODULES = ['test.spiders']
NEWSPIDER_MODULE = 'test.spiders'
ROBOTSTXT_OBEY = True # True遵守机器人协议，False不遵守
ITEM_PIPELINES = {'test.pipelines.TestPipeline':300, }
```



