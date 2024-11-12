from flask import Blueprint, request, jsonify

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')


@pb.route('/text_analysis', methods=['POST'])
def text_analysis():
    result = None
    text = request.form.get('text')
    if text == '测试':
        result = '正面'
    else:
        result = '中性'
    return jsonify(result=result)


@pb.route('/spider_analysis/topic', methods=['POST'])
def spider_analysis_topic():
    result = None
    url = request.form.get('url')
    cookie = request.form.get('cookie')
    keyword = request.form.get('keyword')

    # 这里可以根据 URL、COOKIE 和关键词来进行相应的分析逻辑
    analysis_result = {
        'url': url,
        'cookie': cookie,
        'keyword': keyword,
        'discussion_count': 120,
        'participant_count': 45,
        'popularity_score': 7.8,
        'sentiment': '积极'
    }
    return jsonify(result=analysis_result)




