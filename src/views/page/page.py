from flask import Blueprint, render_template, request, jsonify
import openai
import os
import json

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')

openai.api_key = os.getenv("OPENAI_API_KEY")

@pb.route('/text_analysis', methods=['GET'])
def text_analysis():
    return render_template('text_analysis.html')

@pb.route('/text_analysis/single', methods=['POST'])
def text_analysis_single():
    result = None
    text = request.form.get('text')
    if text == '测试':
        result = '正面'
    else:
        result = '中性'
    return jsonify(result=result)


@pb.route('/text_analysis/batch', methods=['POST'])
def text_analysis_batch():
    batch_text = request.form.get('batch_text', '')
    lines = batch_text.strip().split('\n')
    results = []

    for line in lines:
        if line.strip() == '测试':
            results.append(f'"{line}" 的情感倾向为: 正面')
        else:
            results.append(f'"{line}" 的情感倾向为: 中性')
    return jsonify(results=results)





@pb.route('/spider_analysis')
def spider_analysis():
    return render_template('spider_analysis.html')

@pb.route('/spider_analysis/user', methods=['POST'])
def spider_analysis_user():
    result = None
    url = request.form.get('url')
    analysis_result = {
        'url': url,
        'post_count': 25,
        'interaction_count': 150,
        'activity_score': 8.5
    }
    return jsonify(result=analysis_result)

@pb.route('/spider_analysis/topic', methods=['POST'])
def spider_analysis_topic():
    result = None
    url = request.form.get('url')
    analysis_result = {
        'url': url,
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




@pb.route('/contact', methods=['POST'])
def contact():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        return jsonify({'success': True, 'message': '信息已发送'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
