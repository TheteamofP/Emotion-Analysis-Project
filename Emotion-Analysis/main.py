import  subprocess
from weibo_crawler.weibo_crawler.update_settings import main
from nlp.text_processor import text_processor
from data_visualization.wordcloud_generator import wordclouds_generator


def emotion_analyzer(cookie, keywords, start_date, end_date, regions,
                     weibo_type_input, contain_type_input):
    main(cookie, keywords, start_date, end_date, regions, weibo_type_input,
         contain_type_input)

    subprocess.run(['cd weibo_crawler', 'scrapy crawl search'])

    text_processor()

    wordclouds_generator()



