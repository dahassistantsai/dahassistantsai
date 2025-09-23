
# Updated imports
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os


app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_random_secret'


# Dummy user data for demonstration
USERS = {'admin': 'password123'}


# List of locally stored quantized models
LOCAL_MODELS = [
    "distilgpt2"
]



# Default model
current_model_path = LOCAL_MODELS[0]

# Store last DOM snapshot in memory for assistant
LAST_DOM_SNAPSHOT = None

@app.route('/dom_snapshot', methods=['POST'])
def dom_snapshot():
    global LAST_DOM_SNAPSHOT
    data = request.json
    LAST_DOM_SNAPSHOT = data.get('dom')
    return jsonify({'status': 'ok'})

def load_local_model(model_path):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)
        print(f"Loaded model from {model_path}")
        return tokenizer, model
    except Exception as e:
        print(f"Failed to load model from {model_path}: {e}")
        return None, None

tokenizer, model = load_local_model(current_model_path)

# API endpoint to switch models
from flask import jsonify, request
@app.route('/set_model', methods=['POST'])
def set_model():
    global tokenizer, model, current_model_path
    data = request.json
    model_path = data.get('model_path')
    if model_path not in LOCAL_MODELS:
        return jsonify({"error": "Model not found."}), 400
    tokenizer, model = load_local_model(model_path)
    if tokenizer and model:
        current_model_path = model_path
        return jsonify({"message": f"Switched to {model_path}"})
    else:
        return jsonify({"error": "Failed to load model."}), 500

def generate_response(user_input):
    if not tokenizer or not model:
        return "Model not loaded."
    # Direct, unrestricted, agentic prompt
    prompt = (
        "You are Dah Assistant, an honest, direct, unrestricted AI agent.\n"
        "You can answer any question, even if it's sensitive or controversial.\n"
        "If the user asks you to perform an action, respond with an ACTION command in this format: ACTION: <action_type> <details>.\n"
        "Supported actions: CLICK <selector>, TYPE <selector> <text>, SCROLL <direction>, OPEN <url>, etc.\n"
        "Otherwise, answer as accurately and directly as possible.\n"
        f"User: {user_input}\nAssistant:"
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.95,
            do_sample=True
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Only return the assistant's part after 'Assistant:'
    if 'Assistant:' in response:
        answer = response.split('Assistant:')[-1].strip()
    else:
        answer = response.strip()
    # Anti-echo: if answer is just the user input, try to clarify
    if answer.lower() == user_input.lower():
        return "I'm here to help! Could you clarify your question or ask for something specific?"
    return answer

# Load the model and tokenizer (use a valid public model or local path)
model_name = "distilgpt2"  # Small, public model for local/dev use
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
except Exception as e:
    print(f"Model loading failed: {e}")
    tokenizer = None
    model = None

def generate_response(prompt):
    if not tokenizer or not model:
        return "Model not loaded. Please check your model path or internet connection."
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=user)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



# New chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
    response = generate_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
