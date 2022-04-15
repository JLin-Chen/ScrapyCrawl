# ScrapyCrawl

This is a repository that records the codes and issues met when running a project for scrapy crawl. 

# 一、Scrapy框架的建立

## 1. 框架图

![project_menu](/img/project_menu.bmp)

## 2. 新建一个爬虫项目

· 使用PyCharm新建一个项目

· 设置项目Setting，Project Interpreter， Install scrapy

· 打开控制台cmd，cd命令转到项目Scripts所在地址，输入“scrapy startproject test1”  
  如：
  
```cmd
D:\>cd D:\PyCharm_Python\test\venv\Scripts

D:\PyCharm_Python\test\venv\Scripts>scrapy startproject test
```

· 根据需要修改items.py/pipelines.py/settings.py

* 详细代码样例[查看](/lianjia)



# 二、反爬机制的解决方案

当我们遇到目标网站的反爬机制的时候，常见的报错为： DEBUG: Crawled (403) ，即网站采用了防爬技术anti-web-crawling technique。

在[解决方案](/anti_crawling)中，我们会由浅入深归纳总结常用的可行的对抗反爬措施的方法。


 # 涉及CSV的操作指南
 
 爬虫得到的数据通常需要经过一定的数据清洗才可使用，[CSV](/csv)记录了常用的csv文件处理及数据清洗操作。
 

# 踩坑解决方案

1. DEBUG: Crawled (200) ：代表网站成功访问，但是页面获取信息出错，检查JS或者Xpath相关路径是否出错。  

2. DEBUG: Crawled (403) ：代表表示网站采用了防爬技术anti-web-crawling technique。
    
3. request无法利用Xpath提取到数据：开发者工具中显示的HTML代码和网页真正的源代码存在区别，可能数据并不在网页源代码中，所以爬不到数据。（tbody节点的影响？使用Xpath Helper时也许能爬到？）
    网站的原始代码可能会被chrome浏览器自动修正。
    
4. scrapy默认是多线程自动执行的，这样可以提高爬虫的运行效率。但是，如果遇到一些爬虫项目涉及多重循环和变量间的统一参数传递的话，多线程访问同一变量会因为线程执行时间不同而导致结果的不同。在这种情况下，需要在settings.py中，手动设置线程为1，可使得所有的爬取按照顺序和逻辑进行。（如uswoo的streeteasy爬虫项目）
 ```python
# 多线程爬取会导致异步乱序问题
# 决定最大值
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# 下面两个二选一，一个是针对域名设置并发，一个是针对IP设置并发
CONCURRENT_REQUESTS_PER_IP = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
```

 
 
