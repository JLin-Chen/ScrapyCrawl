在本篇文章中，我们将会介绍一些实用可行的解决目标网站反爬机制的措施。

# 一、需要了解掌握的爬虫编程习惯

1. 在代码的关键地方调用time.sleep降低爬虫对目标网站的请求频率，可以加上random函数随机设置访问时间间隔，以便使得爬虫更像人工操作。
```python
import time
import random

sleeptime = random.randint(0, 10)  # 返回[0,10]之间的任意整数
time.sleep(sleeptime)
```

2. 大多数网站都会要求爬虫遵守ROBOTS协议，即“盗亦有道”，划定爬虫可爬取的范围，不得访问网站的敏感数据。然而，很多时候我们写的爬虫都会在ROBOTS协议规定的范围外，所以我们通常要在settings.py中设置：
```python
ROBOTSTXT_OBEY = False
```
并且为了防止IP被ban，通常仅做小范围小数据量的爬取以做测试、学习和试验用。

上述的方案仅作基础的爬虫编程习惯用，一般情况下解决不了目标网站的反爬机制，所以在上述要点的基础上，展开以下解决方案的讨论。

# 二、进阶反反爬

__1. 用户代理信息User-Agent__

  对于比较简单的情景来说，设置用户代理则可以模拟不同的浏览器访问场景，绕过网站的反爬封锁。

  法1：尝试在请求头部构造User Agent。

    ```python
    def start_requests(self): 

        yield Request("http://www.php.cn/", headers={'User-Agent': "your agent string"})
    ```

  法2：setting中添加：

    ```python
    USER_AGENT = "your agent string"
    
    ```

__2. 网站cookie信息__
  
  尝试添加网站的cookie信息可以模拟用户登录，更易进入目标网站进行爬取。
  
  法1：在spider.py文件中加上含cookie的header头。
    
    ```python
    cookie=['your cookie string']
    header = {
    'User-Agent': 'your agent string',
    'Connection': 'keep-alive',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cookie': cookie}
    
     def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,headers=header, callback=self.parse)
     ```
     
__3. 代理IP的设置__


  
