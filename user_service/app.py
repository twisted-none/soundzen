from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

USER_SERVICE_PORT = 5001
PROJECT_SERVICE_URL = os.getenv('PROJECT_SERVICE_URL', 'http://project-service:5000')

@app.route('/users', methods=['GET'])
def get_users():
    """Возвращает список пользователей"""
    users = [
        {"id": 1, "name": "Иван Иванов", "email": "ivan@example.com"},
        {"id": 2, "name": "Петр Петров", "email": "petr@example.com"},
        {"id": 3, "name": "Мария Сидорова", "email": "maria@example.com"}
    ]
    return jsonify(users)

@app.route('/send-to-project', methods=['POST'])
def send_to_project():
    """Отправляет данные пользователей в основной проект"""
    try:
        users_response = get_users()
        users_data = users_response.json
        
        # Отправляем данные в основной проект
        response = requests.post(
            f"{PROJECT_SERVICE_URL}/receive-users",
            json=users_data
        )
        
        return jsonify({
            "message": "Данные отправлены в проект",
            "status": response.status_code,
            "sent_data": users_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=USER_SERVICE_PORT, debug=True)