from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Chat and user data
chats = []
users = {}

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_chats')
def get_chats():
    return jsonify(chats)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    username = data['username']
    message = data['message']
    chats.append({'username': username, 'message': message})
    return jsonify({'status': 'Message sent'})

@app.route('/upload', methods=['POST'])
def upload():
    if 'media' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['media']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    chats.append({'username': 'Media', 'message': f'<img src="/{filename}" alt="Media">'})
    return jsonify({'status': 'File uploaded'})

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()
    username = data['username']
    status = data['status']
    users[username] = {'status': status}
    return jsonify({'status': 'Status updated'})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host='0.0.0.0', port=5000)