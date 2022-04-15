import scrapy
import pandas as pd
import csv
import time
import random
from test1.items import Test1Item

'''爬取初始网页信息'''
# ----爬取初始网页信息-----
class Test1Spider(scrapy.spiders.Spider):
    name = "test1"
    allowed_domains = ["streeteasy.com"]
    df = pd.read_csv('link_info.csv', encoding='utf-8')
    # 初始化各属性列表
    num_url=-1
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


    def start_requests(self):
        for url in self.start_urls:
            cookie = '_actor=eyJpZCI6ImFUcThHbzNrem52eTRXY21qb1plekE9PSJ9--99dde6080d243d48cee1a2d0de9f0599b6b946b8; _se_t=2a1b50ea-e246-49ae-8d05-9fe9431fff48; _gcl_au=1.1.1212773542.1648708179; _ga=GA1.2.1302664899.1648708179; _pxvid=f24f9896-b0bb-11ec-ab6f-6e454e757a7a; zg_anonymous_id="8c924406-573a-42b8-b839-c058798a468e"; zjs_anonymous_id="2a1b50ea-e246-49ae-8d05-9fe9431fff48"; g_state={"i_l":0}; zjs_user_id="8480089"; __gads=ID=02755dc2f56e1490:T=1648708229:S=ALNI_MYQAm3pqdbIM8XNhw0fe42dOsj64Q; __gpi=UID=00000457a1578291:T=1648794941:RT=1648794941:S=ALNI_MaAp1S9clj9EAWCCQ-BkqTxjJBD_Q; _gid=GA1.2.1292094018.1648882468; _gcl_aw=GCL.1648908509.Cj0KCQjw6J-SBhCrARIsAH0yMZi5IKmovlkSYukm4ewdMn2BlE_lrb9Hv-xIDZr7unlBP39dvMaDw8caAvEgEALw_wcB; _gac_UA-122241-1=1.1648908511.Cj0KCQjw6J-SBhCrARIsAH0yMZi5IKmovlkSYukm4ewdMn2BlE_lrb9Hv-xIDZr7unlBP39dvMaDw8caAvEgEALw_wcB; ki_r=; KruxPixel=true; _uetsid=4069e320b33411ecbff3635df2c0c641; _uetvid=999c0ea0b0ca11ec9b1f91c40fa79e87; pxcts=9565ad31-b3ba-11ec-af25-6b4548767267; _pxff_rf=1; _pxff_fp=1; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczRORGd3TURnNVhTd2lTek5GYnpVMVluaGxlVTR4ZUZjNFNsWmFYMklpTENJeE5qUTVNRE0zTkRZd0xqWXlNVGM1TlRjaVhRPT0iLCJleHAiOiIyMDMyLTA0LTA0VDAxOjU3OjQwWiIsInB1ciI6bnVsbH19--9993eb2a9bf2ebb788cd100fd19de6a062382da4; se_lsa=2022-04-03+21:57:40+-0400; user_auth_token=-r17ieBhspc262yZUFfK; _ses=K0kyaVJJb084QzM0OTQvcHhFdHlFNmpGNXUvTWZ6L0hid3pUM1c2SGhHQ29vb2g5dThEcXYxTWhoNmRPZytWU016ZGhBOHJsTGJTRVJ6cjYybzVMdmVsTExJT1hSV08wd0tzWVBGY3crb1hsNUtUQlRzT1p3ZlRYZDlsVjdPVnp3NkhLSk9uRXM0Wkh6NWpXZTEzQW1ZZnRpUDBsU3ZnckV2QVlVa3B4aUNrUG1UcFovTXE4YkE2KzE1MHc0S3lKWHdncWsxT1R0U01BZFpkdG1GNnBPUT09LS1hbHFBMFh5K1lMTnVNTGhWZVZ6OW5BPT0=--bbaaee66acca63a9f7e6a671e5378caeb4e5012e; _dc_gtm_UA-122241-1=1; _px3=6e93977d918d43f648b06907d2deb4c0ee9fde2b390f74d51de1ef9fdd2c17c9:Nq1udXw03tW/JFncO1StEMHjwA0N+RSXRwND1ZWqoDJC+vhG8vS3/6qfdK4lKx+Xf26VUtV/4qcoxv7bG44SNw==:1000:QLfEkiwGvo2277YqeB8IakFYzstUSxKU2Xqhfq8BEkkOHeYnxCs7VMWcKUJui+rtaIhFTuNGo7wZ1q8rgyIGDhBtr/W7VaqzaQZ3Sx0ELlEVtTRpQyb8h/Uc5RVKWQA7bSWq1Sd8SAf+tmZWvjkYbG9mp1pQTlvLm4A//bH6cjd1tSKJ0nSCQbMJn/CxR+bSPYqbBShXU8GAlRA89dydwQ==; ki_t=1648708184732;1649037464518;1649037464518;5;74; google_one_tap=0'
            Cookie = {'Cookie':cookie}
            sleeptime = random.randint(0, 10)
            time.sleep(sleeptime)
            yield scrapy.Request(url=url,cookies=Cookie,callback=self.parse)


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



'''爬取跳转网页信息'''
# # ------爬取跳转网页信息------
# class Test1Spider(scrapy.spiders.Spider):
#     name = "test1"
#     allowed_domains = ["streeteasy.com"]
#     df = pd.read_csv('house_info_clean.csv', encoding='utf-8')
#     # 初始化各属性列表
#     num_url=-1
#     start_urls = []
#     building_name = []
#     xpath_unit = []
#     xpath_beds = []
#     xpath_baths = []
#     xpath_price = []
#     length = len(df)
#     for i in range(length):
#         start_urls.append(df['url_py_add'][i])
#         building_name.append(df['building_name'][i])
#         xpath_unit.append(df['unit'][i])
#         xpath_beds.append(df['beds'][i])
#         xpath_baths.append(df['baths'][i])
#         xpath_price.append(df['price'][i])
#
#
#     def start_requests(self):
#         for url in self.start_urls:
#             cookie = '_actor=eyJpZCI6ImFUcThHbzNrem52eTRXY21qb1plekE9PSJ9--99dde6080d243d48cee1a2d0de9f0599b6b946b8; _se_t=2a1b50ea-e246-49ae-8d05-9fe9431fff48; _gcl_au=1.1.1212773542.1648708179; _ga=GA1.2.1302664899.1648708179; _pxvid=f24f9896-b0bb-11ec-ab6f-6e454e757a7a; zg_anonymous_id="8c924406-573a-42b8-b839-c058798a468e"; zjs_anonymous_id="2a1b50ea-e246-49ae-8d05-9fe9431fff48"; g_state={"i_l":0}; zjs_user_id="8480089"; __gads=ID=02755dc2f56e1490:T=1648708229:S=ALNI_MYQAm3pqdbIM8XNhw0fe42dOsj64Q; __gpi=UID=00000457a1578291:T=1648794941:RT=1648794941:S=ALNI_MaAp1S9clj9EAWCCQ-BkqTxjJBD_Q; _gid=GA1.2.1292094018.1648882468; _gcl_aw=GCL.1648908509.Cj0KCQjw6J-SBhCrARIsAH0yMZi5IKmovlkSYukm4ewdMn2BlE_lrb9Hv-xIDZr7unlBP39dvMaDw8caAvEgEALw_wcB; _gac_UA-122241-1=1.1648908511.Cj0KCQjw6J-SBhCrARIsAH0yMZi5IKmovlkSYukm4ewdMn2BlE_lrb9Hv-xIDZr7unlBP39dvMaDw8caAvEgEALw_wcB; ki_r=; KruxPixel=true; _uetsid=4069e320b33411ecbff3635df2c0c641; _uetvid=999c0ea0b0ca11ec9b1f91c40fa79e87; pxcts=9565ad31-b3ba-11ec-af25-6b4548767267; _pxff_rf=1; _pxff_fp=1; remember_user_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IlcxczRORGd3TURnNVhTd2lTek5GYnpVMVluaGxlVTR4ZUZjNFNsWmFYMklpTENJeE5qUTVNRE0zTkRZd0xqWXlNVGM1TlRjaVhRPT0iLCJleHAiOiIyMDMyLTA0LTA0VDAxOjU3OjQwWiIsInB1ciI6bnVsbH19--9993eb2a9bf2ebb788cd100fd19de6a062382da4; se_lsa=2022-04-03+21:57:40+-0400; user_auth_token=-r17ieBhspc262yZUFfK; _ses=K0kyaVJJb084QzM0OTQvcHhFdHlFNmpGNXUvTWZ6L0hid3pUM1c2SGhHQ29vb2g5dThEcXYxTWhoNmRPZytWU016ZGhBOHJsTGJTRVJ6cjYybzVMdmVsTExJT1hSV08wd0tzWVBGY3crb1hsNUtUQlRzT1p3ZlRYZDlsVjdPVnp3NkhLSk9uRXM0Wkh6NWpXZTEzQW1ZZnRpUDBsU3ZnckV2QVlVa3B4aUNrUG1UcFovTXE4YkE2KzE1MHc0S3lKWHdncWsxT1R0U01BZFpkdG1GNnBPUT09LS1hbHFBMFh5K1lMTnVNTGhWZVZ6OW5BPT0=--bbaaee66acca63a9f7e6a671e5378caeb4e5012e; _dc_gtm_UA-122241-1=1; _px3=6e93977d918d43f648b06907d2deb4c0ee9fde2b390f74d51de1ef9fdd2c17c9:Nq1udXw03tW/JFncO1StEMHjwA0N+RSXRwND1ZWqoDJC+vhG8vS3/6qfdK4lKx+Xf26VUtV/4qcoxv7bG44SNw==:1000:QLfEkiwGvo2277YqeB8IakFYzstUSxKU2Xqhfq8BEkkOHeYnxCs7VMWcKUJui+rtaIhFTuNGo7wZ1q8rgyIGDhBtr/W7VaqzaQZ3Sx0ELlEVtTRpQyb8h/Uc5RVKWQA7bSWq1Sd8SAf+tmZWvjkYbG9mp1pQTlvLm4A//bH6cjd1tSKJ0nSCQbMJn/CxR+bSPYqbBShXU8GAlRA89dydwQ==; ki_t=1648708184732;1649037464518;1649037464518;5;74; google_one_tap=0'
#             Cookie = {'Cookie':cookie}
#             sleeptime = random.randint(0, 10)
#             time.sleep(sleeptime)
#             yield scrapy.Request(url=url,cookies=Cookie,callback=self.parse)
#
#
#     def parse(self, response):
#         item = Test1Item()
#         self.num_url = self.num_url + 1
#         sleeptime = random.randint(0, 10)
#         time.sleep(sleeptime)
#         item['building_name'] = self.building_name[self.num_url]
#         item['unit'] = self.xpath_unit[self.num_url]
#         item['beds'] = self.xpath_beds[self.num_url]
#         item['baths'] = self.xpath_baths[self.num_url]
#         item['price'] = self.xpath_price[self.num_url]
#         item['price_min'] = response.xpath('//*[@id="content"]/main/div[3]/article[2]/section[1]/div/div[2]/ul/li[1]/p/text()').extract()
#         print(item['building_name'])
#         print(item['price_min'])
#         # if item['building_name'and'unit'and'beds'and'baths'and'price']:
#         #
#         #     yield item




