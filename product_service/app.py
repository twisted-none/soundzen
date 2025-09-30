from flask import Flask, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

PRODUCT_SERVICE_PORT = 5002
PROJECT_SERVICE_URL = os.getenv('PROJECT_SERVICE_URL', 'http://project-service:5000')

@app.route('/products', methods=['GET'])
def get_products():
    """Возвращает список продуктов"""
    products = [
        {"id": 1, "name": "Ноутбук", "price": 50000, "category": "Электроника"},
        {"id": 2, "name": "Смартфон", "price": 30000, "category": "Электроника"},
        {"id": 3, "name": "Книга", "price": 500, "category": "Литература"}
    ]
    return jsonify(products)

@app.route('/send-to-project', methods=['POST'])
def send_to_project():
    """Отправляет данные продуктов в основной проект"""
    try:
        products_response = get_products()
        products_data = products_response.json
        
        # Добавляем временную метку
        enriched_data = {
            "products": products_data,
            "timestamp": datetime.now().isoformat(),
            "service": "product-service"
        }
        
        # Отправляем данные в основной проект
        response = requests.post(
            f"{PROJECT_SERVICE_URL}/receive-products",
            json=enriched_data
        )
        
        return jsonify({
            "message": "Данные продуктов отправлены в проект",
            "status": response.status_code,
            "sent_data": enriched_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервиса"""
    return jsonify({"status": "healthy", "service": "product-service"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PRODUCT_SERVICE_PORT, debug=True)