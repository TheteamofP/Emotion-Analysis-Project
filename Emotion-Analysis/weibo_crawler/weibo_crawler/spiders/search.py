import csv
import sys
from datetime import datetime,timedelta
from ..utils.util import standardize_date
import scrapy
from scrapy.utils.project import get_project_settings

from ..utils.region import region_dict


class SearchSpider(scrapy.Spider):
    name = "search"
    allowed_domains = ["weibo.com"]
    settings = get_project_settings()
    further_threshold = settings.get('FURTHER_THRESHOLD', 46)     # 设置阈值，当微博数量超过该值时细分请求

    #基本utl
    base_url = 'https://s.weibo.com/weibo?q='

    # 从设置中获取关键词列表和其他配置
    keyword_list =settings.get('KEYWORD_LIST')
    weibo_type = settings.get('WEIBO_TYPE', '')
    contain_type = settings.get('CONTAINER_TYPE', '')
    regions = settings.get('REGIONS', [])



    #处理关键词中话题标记
    for i, keyword in enumerate(keyword_list):
        if len(keyword) > 2 and keyword[0] == '#' and keyword[-1] == '#':
            keyword_list[i] = '%23' + keyword[1:-1] + '%23'

    def __init__(self, *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        # 初始化 CSV 文件和写入器
        self.file = open('weibo_data.csv', mode='w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.file)
        # 定义 CSV 文件的列标题
        self.csv_writer.writerow(['keyword', 'region', 'id', 'user', 'text', 'created_at', 'source'])

    def start_requests(self):
        # #基本utl
        # base_url = 'https://s.weibo.com/weibo?q='

        #日期处理
        start_date = datetime.strptime(self.settings.get('START_DATE', datetime.now().strftime('%Y-%m-%d')),'%Y-%m-%d')
        end_date = datetime.strptime(self.settings.get('END_DATE', datetime.now().strftime('%Y-%m-%d')),'%Y-%m-%d')

        # 日期检查：确保 start_date 不晚于 end_date
        if start_date > end_date:
            sys.exit('settings.py配置错误，START_DATE值应早于或等于END_DATE值，请重新配置settings.py')

        # 将 end_date 增加一天以确保包含终止日期的完整数据
        end_date += timedelta(days=1)

        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')

        # 构建请求 URL
        for keyword in self.keyword_list:
            #如果不需要地区限制
            if not self.regions or '全部' in self.regions:
                url = f"{self.base_url}{keyword}{self.weibo_type}{self.contain_type}&timescope=custom:{start_str}:{end_str}"
                print(f"Request URL without region: {url}")  # 输出 URL
                yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword})
            else:
                # 针对每个区域构建请求 URL
                for region_name in self.regions:
                    region_info = region_dict.get(region_name)
                    if region_info:
                        region_code = region_info["code"]
                        region_url = f"{self.base_url}{keyword}&region=custom:{region_code}:1000{self.weibo_type}{self.contain_type}&timescope=custom:{start_str}:{end_str}"
                        print(f"Request URL with region {region_name}: {region_url}")  # 输出 URL

                        yield scrapy.Request(url=region_url, callback=self.parse,
                                             meta={'keyword': keyword, 'region': region_name})
                    else:
                        print(f"Warning: 未找到 {region_name} 的地区信息，请检查 REGION 配置是否正确")

    def parse(self, response):
        """按天解析"""
        keyword = response.meta.get('keyword')
        region = response.meta.get('region', '全部')

        # 解析微博数据
        for weibo in self.parse_weibo(response):
            yield weibo

        # 检查是否有下一页
        next_url = response.xpath('//a[@class="next"]/@href').get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'keyword': keyword, 'region': region})
        else:
            # 页面微博数量是否超过阈值，如果超过则进一步细分按天处理
            page_count = len(response.xpath('//ul[@class="s-scroll"]/li'))
            if page_count >= self.further_threshold:
                start_date = datetime.strptime(self.settings.get('START_DATE'), '%Y-%m-%d')
                end_date = datetime.strptime(self.settings.get('END_DATE'), '%Y-%m-%d')
                current_date = start_date
                while current_date <= end_date:
                    next_day = current_date + timedelta(days=1)
                    start_str = current_date.strftime('%Y-%m-%d')
                    end_str = next_day.strftime('%Y-%m-%d')
                    url = f"{self.base_url}{keyword}&timescope=custom:{start_str}:{end_str}"
                    yield scrapy.Request(url=url, callback=self.parse_by_day,
                                         meta={'keyword': keyword, 'region': region})
                    current_date = next_day

    def parse_by_day(self, response):
        """按天进一步细分，处理分页及按小时细分"""
        keyword = response.meta.get('keyword')
        date = response.meta.get('date')
        region = response.meta.get('region', '全部')

        # 提取当前页面的微博数据
        for weibo in self.parse_weibo(response):
            yield weibo

        # 检查是否有下一页
        next_url = response.xpath('//a[@class="next"]/@href').get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_by_day,
                meta={'keyword': keyword, 'date': date, 'region': region}
            )
        else:
            # 如果没有下一页，则按小时细分请求
            start_date = datetime.strptime(date, '%Y-%m-%d')
            for hour in range(24):
                start_time = start_date.replace(hour=hour).strftime('%Y-%m-%d-%H')
                end_time = start_date.replace(hour=hour + 1).strftime('%Y-%m-%d-%H')
                url = f"{response.meta['base_url']}{self.weibo_type}{self.contain_type}&timescope=custom:{start_time}:{end_time}&page=1"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_by_hour,
                    meta={'keyword': keyword, 'start_time': start_time, 'end_time': end_time, 'region': region}
                )

    def parse_by_hour(self, response):
        """以小时为单位解析微博数据"""
        keyword = response.meta.get('keyword')
        start_time = response.meta.get('start_time')
        end_time = response.meta.get('end_time')
        region = response.meta.get('region', '全部')
        #依次解析微博数据
        for weibo in self.parse_weibo(response):
            yield weibo
        #分页处理
        next_url = response.xpath('//a[@class="next"]/@href').get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_by_hour, meta={'keyword': keyword, 'region': region})

    def parse_by_hour_province(self, response):
        """按小时和省级地区进行微博数据抓取与分页解析"""
        keyword = response.meta.get('keyword')
        start_time = response.meta.get('start_time')
        end_time = response.meta.get('end_time')
        province = response.meta.get('province')
        for weibo in self.parse_weibo(response):
            yield weibo
        next_url = response.xpath('//a[@class="next"]/@href').get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_by_hour_province,
                                 meta={'keyword': keyword, 'province': province})

    def parse_weibo(self, response):
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
            txt_sel = sel.xpath('.//p[@class="txt"]')[0]
            content_full = sel.xpath('.//p[@node-type="feed_list_content_full"]')
            is_long_weibo = False

            # 如果存在长微博内容
            if content_full:
                txt_sel = content_full[0]
                is_long_weibo = True

            weibo['text'] = txt_sel.xpath('string(.)').get().replace('\u200b', '').replace('\ue627', '').strip()
            if is_long_weibo:
                weibo['text'] = weibo['text'][:-4]  # 移除长微博末尾的省略符
            # 发布时间和来源
            created_at = sel.xpath(
                './/div[@class="from"]/a[1]/text()').extract_first(
            ).replace(' ', '').replace('\n', '').split('前')[0]
            weibo['created_at'] = standardize_date(created_at) if created_at else None
            weibo['source'] = sel.xpath('.//div[@class="from"]/a[2]/text()').get()

            # 打印微博信息，验证数据抓取是否成功
            print(weibo)
            self.csv_writer.writerow(weibo.values())
            yield weibo

    def close(self, reason):
        # 关闭 CSV 文件
        self.file.close()
