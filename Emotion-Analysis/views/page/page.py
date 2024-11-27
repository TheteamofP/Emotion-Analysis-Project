from flask import Blueprint, request, jsonify
import openai
import os
import json

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')


@pb.route('/text_analysis', methods=['POST'])
def text_analysis():
    text = request.form.get('text')
    if text == '测试':
        result = '正面'
    else:
        result = '中性'
    return jsonify(result=result)


@pb.route('/spider_analysis/topic', methods=['POST'])
def spider_analysis_topic():
    cookie = request.form.get('cookie')
    keywords = request.form.get('keyword')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    regions = request.form.get('regions')
    weibo_type_input = request.form.get('weibo_type_input')
    contain_type_input = request.form.get('contain_type_input')

    from main import emotion_analyzer
    result = emotion_analyzer(cookie, keywords, start_date, end_date, regions,
                              weibo_type_input, contain_type_input)

    from data_visualization.question_generator import question_generator
    question = question_generator()
    print(question)

    analysis_result = {
        'cookie': cookie,
        'keyword': keywords,
        'start_date': start_date,
        'end_date': end_date,
        'regions': regions,
        'weibo_type': weibo_type_input,
        'contain_type': contain_type_input,
        'question': question
    }

    if result == 1:
        return jsonify({'status': 'success', 'result': analysis_result})
    else:
        return jsonify({'status': 'failed', 'message': '情绪分析未成功完成'})


@pb.route('/gpt_suggestion', methods=['GET', 'POST'])
def gpt_suggestion():
    preset_text = request.args.get('text', '')
    user_input = request.form.get('text') or preset_text

    if not user_input:
        return jsonify(result={'error': '未提供输入文本'})

    try:
        chat_history = json.loads(request.form.get('history', '[]'))

        messages = [{"role": "assistant" if msg['type'] == 'ai' else "user", "content": msg['content']}
                    for msg in chat_history[-10:]]

        messages.append({"role": "user", "content": user_input})

        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_API_BASE")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )

        gpt_response = response['choices'][0]['message']['content'].strip()
        return jsonify(result={'gpt_response': gpt_response})

    except openai.error.OpenAIError as e:
        return jsonify(result={'error': f"GPT API 调用出错: {str(e)}"})
    except Exception as e:
        return jsonify(result={'error': f"出现未知错误: {str(e)}"})
