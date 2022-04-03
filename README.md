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

 # 涉及从CSV的操作指南
 
 爬虫得到的数据通常需要经过一定的数据清洗才可使用，[CSV](/csv)记录了常用的csv文件处理及数据清洗操作。
 

# 踩坑解决方案

1. DEBUG: Crawled (200) ：代表网站成功访问，但是页面获取信息出错，检查JS或者Xpath相关路径是否出错。  

2. DEBUG: Crawled (403) ：代表表示网站采用了防爬技术anti-web-crawling technique，比较简单即会检查用户代理（User Agent）信息。记得robot协议设置为False。

    尝试在请求头部构造User Agent。

    ```python
    def start_requests(self): 

        yield Request("http://www.php.cn/", 

                      headers={'User-Agent': "your agent string"})
    ```

    或者在setting中添加：

    ```python
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    ```
 3. request无法利用Xpath提取到数据：开发者工具中显示的HTML代码和网页真正的源代码存在区别，可能数据并不在网页源代码中，所以爬不到数据。（tbody节点的影响？使用Xpath Helper时也许能爬到？）
    网站的原始代码可能会被chrome浏览器自动修正。
 
 
