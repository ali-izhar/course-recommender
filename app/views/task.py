from flask import Blueprint, render_template, request, session, jsonify, current_app
from app.api import chat_completion, Recommender

task_bp = Blueprint('task', __name__, url_prefix='/task')


@task_bp.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        prompt = request.form['prompt']
        
        # Create the Recommender within the application context
        with current_app.app_context():
            recommendation_model = Recommender()
            
        courses = recommendation_model.recommend(prompt)
        return render_template('result.html', sender='model', courses=courses)
    return render_template('index.html')


@task_bp.route('/gpt', methods=['GET', 'POST'])
def gpt():
    if request.method == 'POST':
        if request.is_json:
            prompt = request.json['prompt']
        else:
            prompt = request.form['prompt']

        # Retrieve the conversation history from the session
        conversation = session.get('conversation', [])
        conversation.append({"role": "user", "content": prompt})

        response = chat_completion(prompt)
        conversation.append({"role": "ai", "content": response})
        session['conversation'] = conversation

        if request.is_json:
            # Return JSON if request is made via AJAX
            return jsonify(response=response, conversation=conversation)
        else:
            return render_template('result.html', sender='gpt', conversation=conversation)

    return render_template('index.html')


@task_bp.route('/clear_conversation', methods=['POST'])
def clear_conversation():
    session['conversation'] = []
    return jsonify(success=True)