from datetime import datetime, timedelta
from time import strftime
import scrapy
from scrapy.utils.project import get_project_settings


class SearchSpider(scrapy.Spider):
    name = "search"
    allowed_domains = ["weibo.com"]
    settings = get_project_settings()

    keyword_list = settings.get('KEYWORD_LIST')
    # regions = settings.get('REGIONS')

    #处理关键词中话题标记
    for i, keyword in enumerate(keyword_list):
        if len(keyword) > 2 and keyword[0] == '#' and keyword[-1] == '#':
            keyword_list[i] = '%23' + keyword[1:-1] + '%23'

    def start_requests(self):
        # 从设置中获取关键词列表和其他配置
        keyword_list = self.settings.get('KEYWORD_LIST')
        weibo_type = self.settings.get('WEIBO_TYPE', '')
        contain_type = self.settings.get('CONTAINER_TYPE', '')
        regions = self.settings.get('REGIONS', {})

        #基本utl
        base_url = 'https://s.weibo.com/weibo?q='

        #日期处理
        start_date = datetime.strptime(self.settings.get('START_DATE', datetime.now().strftime('%Y-%m-%d')),'%Y-%m-%d')
        end_date = datetime.strptime(self.settings.get('END_DATE', datetime.now().strftime('%Y-%m-%d')),'%Y-%m-%d') + timedelta(days=1)
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')

        # 构建请求 URL
        for keyword in keyword_list:
            #如果不需要地区限制
            if not regions or '全部' in regions:
                url = f"{base_url}{keyword}{weibo_type}{contain_type}&timescope=custom:{start_str}:{end_str}"
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword})
            else:
                # 针对每个区域构建请求 URL
                for region_code, region_name in regions.items():
                    region_url = f"{base_url}{keyword}&region=custom:{region_code}:1000{weibo_type}{contain_type}&timescope=custom:{start_str}:{end_str}"
                    yield scrapy.Request(url=region_url, callback=self.parse,
                                         meta={'keyword': keyword, 'region': region_name})

    def parse(self, response):
        keyword = response.meta.get('keyword')
        region = response.meta.get('region', '全部')

        # 解析微博卡片
        for sel in response.xpath("//div[@class='card-wrap']"):
            weibo = {}
            weibo['keyword'] = keyword
            weibo['region'] = region
            # 微博ID和用户信息
            weibo['id'] = sel.xpath('@mid').get()
            weibo['user'] = sel.xpath('.//a[@class="name"]/text()').get()
            # 微博内容
            text_elements = sel.xpath('.//p[@class="txt"]')
            if text_elements:
                weibo['text'] = text_elements[0].xpath('string(.)').get().strip()  # 获取完整微博文本
            else:
                weibo['text'] = None  # 如果没有找到文本元素，则设置为 None
            # 发布时间和来源
            created_at = sel.xpath('.//div[@class="from"]/a[1]/text()').get()
            weibo['created_at'] = created_at.strip() if created_at else None
            weibo['source'] = sel.xpath('.//div[@class="from"]/a[2]/text()').get()

            # 打印微博信息，验证数据抓取是否成功
            print(weibo)
            yield weibo
