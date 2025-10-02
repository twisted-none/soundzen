from flask import Flask, jsonify, request

app = Flask(__name__)

# Тестовые данные продуктов
products = [
    {'id': 1, 'name': 'Ноутбук ASUS', 'price': 65000, 'category': 'Электроника', 'stock': 15},
    {'id': 2, 'name': 'Смартфон Samsung', 'price': 35000, 'category': 'Электроника', 'stock': 25},
    {'id': 3, 'name': 'Клавиатура Logitech', 'price': 3500, 'category': 'Периферия', 'stock': 40},
    {'id': 4, 'name': 'Монитор LG 27"', 'price': 22000, 'category': 'Электроника', 'stock': 10},
    {'id': 5, 'name': 'Мышь Razer', 'price': 2800, 'category': 'Периферия', 'stock': 50},
]

@app.route('/')
def home():
    return jsonify({
        'service': 'Product Service',
        'status': 'running',
        'version': '1.0'
    })

@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    if category:
        filtered = [p for p in products if p['category'].lower() == category.lower()]
        return jsonify(filtered)
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Продукт не найден'}), 404

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = {
        'id': len(products) + 1,
        'name': data.get('name'),
        'price': data.get('price'),
        'category': data.get('category'),
        'stock': data.get('stock', 0)
    }
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'product-service'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)