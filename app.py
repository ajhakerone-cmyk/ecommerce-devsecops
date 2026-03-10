from flask import Flask, render_template, session, jsonify
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Sample product data
products = [
    {
        'id': 1,
        'name': 'Wireless Noise Cancelling Headphones',
        'price': 299.99,
        'original_price': 399.99,
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop',
        'rating': 4.5,
        'reviews': 2345,
        'badge': 'Sale'
    },
    {
        'id': 2,
        'name': 'Smart Watch Series 7',
        'price': 399.99,
        'original_price': 499.99,
        'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop',
        'rating': 4.8,
        'reviews': 1890,
        'badge': 'New'
    },
    {
        'id': 3,
        'name': 'Ultra Slim Laptop Pro',
        'price': 1299.99,
        'original_price': 1499.99,
        'image': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop',
        'rating': 4.7,
        'reviews': 3456,
        'badge': None
    },
    {
        'id': 4,
        'name': '4K Action Camera',
        'price': 199.99,
        'original_price': 299.99,
        'image': 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500&auto=format&fit=crop',
        'rating': 4.3,
        'reviews': 5678,
        'badge': '20% OFF'
    },
    {
        'id': 5,
        'name': 'Premium Bluetooth Speaker',
        'price': 89.99,
        'original_price': 129.99,
        'image': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&auto=format&fit=crop',
        'rating': 4.6,
        'reviews': 4321,
        'badge': 'Best Seller'
    },
    {
        'id': 6,
        'name': 'Gaming Mouse Elite',
        'price': 59.99,
        'original_price': 79.99,
        'image': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=500&auto=format&fit=crop',
        'rating': 4.4,
        'reviews': 7890,
        'badge': None
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=products[:4])

@app.route('/products')
def product_list():
    return render_template('products.html', products=products)

@app.route('/cart')
def cart():
    # Get cart items from session
    cart_items = session.get('cart', [])
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = next((p for p in products if p['id'] == item['id']), None)
        if product:
            product_with_qty = product.copy()
            product_with_qty['quantity'] = item['quantity']
            cart_products.append(product_with_qty)
            total += product['price'] * item['quantity']
    
    return render_template('cart.html', cart_items=cart_products, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    
    # Check if product already in cart
    cart = session['cart']
    found = False
    
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            found = True
            break
    
    if not found:
        cart.append({'id': product_id, 'quantity': 1})
    
    session['cart'] = cart
    session.modified = True
    
    # Calculate total items in cart
    total_items = sum(item['quantity'] for item in cart)
    
    return jsonify({'success': True, 'cart_count': total_items})

@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.json
    product_id = data.get('product_id')
    action = data.get('action')
    
    cart = session.get('cart', [])
    
    if action == 'increase':
        for item in cart:
            if item['id'] == product_id:
                item['quantity'] += 1
                break
    elif action == 'decrease':
        for item in cart:
            if item['id'] == product_id:
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                else:
                    cart.remove(item)
                break
    elif action == 'remove':
        cart = [item for item in cart if item['id'] != product_id]
    
    session['cart'] = cart
    session.modified = True
    
    # Calculate new totals
    total_items = sum(item['quantity'] for item in cart)
    total_price = 0
    for item in cart:
        product = next((p for p in products if p['id'] == item['id']), None)
        if product:
            total_price += product['price'] * item['quantity']
    
    return jsonify({
        'success': True, 
        'cart_count': total_items,
        'total': total_price
    })

if __name__ == '__main__':
    app.run(debug=True)