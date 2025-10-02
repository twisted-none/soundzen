from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user-service:5001')
PRODUCT_SERVICE_URL = os.environ.get('PRODUCT_SERVICE_URL', 'http://product-service:5002')

@app.route('/')
def home():
    return jsonify({
        'message': 'API Gateway работает',
        'endpoints': [
            '/users - получить всех пользователей',
            '/users/<id> - получить пользователя по ID',
            '/products - получить все продукты',
            '/products/<id> - получить продукт по ID',
            '/dashboard - сводная информация'
        ]
    })

@app.route('/users', methods=['GET'])
def get_users():
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users/{user_id}')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products', methods=['GET'])
def get_products():
    try:
        response = requests.get(f'{PRODUCT_SERVICE_URL}/products')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        users_response = requests.get(f'{USER_SERVICE_URL}/users')
        products_response = requests.get(f'{PRODUCT_SERVICE_URL}/products')
        
        return jsonify({
            'total_users': len(users_response.json()),
            'total_products': len(products_response.json()),
            'users': users_response.json(),
            'products': products_response.json()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)