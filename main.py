from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO

from values import keys

app = Flask(__name__)
app.config['SECRET_KEY'] = keys.app_key     # Secret string
CORS(app)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html', title='Chat')


@app.route('/chat/get/previous/<int:id>', methods=['GET', 'POST'])
def chat_previous(id: int) -> list:
    # Sends [{'user_id': , 'message': ,  'date': }, ]

    return jsonify(id)


@app.route('/chat/put/<int:id>', methods=['POST'])
def chat_put(id):
    return jsonify()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
