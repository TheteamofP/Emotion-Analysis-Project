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
    keyword = request.form.get('keyword')

    analysis_result = {
        'cookie': cookie,
        'keyword': keyword,
        'discussion_count': 120,
        'participant_count': 45,
        'popularity_score': 7.8,
        'sentiment': '积极'
    }
    return jsonify(result=analysis_result)


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




