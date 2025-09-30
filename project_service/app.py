from flask import Flask, jsonify, request

app = Flask(__name__)

PROJECT_SERVICE_PORT = 5000

# Хранилище для полученных данных
received_data = {
    "users": [],
    "products": []
}

@app.route('/')
def home():
    """Главная страница проекта"""
    return jsonify({
        "message": "Основной проект принимает данные от микросервисов",
        "endpoints": {
            "receive_users": "/receive-users (POST)",
            "receive_products": "/receive-products (POST)",
            "get_all_data": "/data (GET)"
        }
    })

@app.route('/receive-users', methods=['POST'])
def receive_users():
    """Принимает данные от user-service"""
    try:
        users_data = request.json
        received_data["users"] = users_data
        
        print(f"Получены данные пользователей: {len(users_data)} записей")
        
        return jsonify({
            "message": "Данные пользователей успешно получены",
            "received_count": len(users_data)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/receive-products', methods=['POST'])
def receive_products():
    """Принимает данные от product-service"""
    try:
        products_data = request.json
        received_data["products"] = products_data
        
        print(f"Получены данные продуктов: {len(products_data.get('products', []))} записей")
        
        return jsonify({
            "message": "Данные продуктов успешно получены",
            "received_timestamp": products_data.get('timestamp'),
            "received_count": len(products_data.get('products', []))
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/data', methods=['GET'])
def get_all_data():
    """Возвращает все полученные данные"""
    return jsonify({
        "users_count": len(received_data["users"]),
        "products_count": len(received_data.get("products", {}).get("products", [])),
        "users": received_data["users"],
        "products": received_data["products"]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья основного проекта"""
    return jsonify({"status": "healthy", "service": "project-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PROJECT_SERVICE_PORT, debug=True)