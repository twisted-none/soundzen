from flask import Flask, jsonify, request

app = Flask(__name__)

# Тестовые данные пользователей
users = [
    {'id': 1, 'name': 'Иван Иванов', 'email': 'ivan@example.com', 'role': 'admin'},
    {'id': 2, 'name': 'Мария Петрова', 'email': 'maria@example.com', 'role': 'user'},
    {'id': 3, 'name': 'Алексей Сидоров', 'email': 'alexey@example.com', 'role': 'user'},
    {'id': 4, 'name': 'Елена Кузнецова', 'email': 'elena@example.com', 'role': 'moderator'},
]

@app.route('/')
def home():
    return jsonify({
        'service': 'User Service',
        'status': 'running',
        'version': '1.0'
    })

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'Пользователь не найден'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        'id': len(users) + 1,
        'name': data.get('name'),
        'email': data.get('email'),
        'role': data.get('role', 'user')
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'user-service'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)