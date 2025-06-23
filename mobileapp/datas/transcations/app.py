import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
NUM_SHOPS = 50
NUM_PRODUCTS = 200
NUM_TRANSACTIONS = 10000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 12, 31)

# Generate synthetic shops
shops = pd.DataFrame({
    'shop_id': range(1, NUM_SHOPS+1),
    'city': np.random.choice(['Kathmandu', 'Pokhara', 'Biratnagar', 'Lalitpur', 'Bhaktapur'], NUM_SHOPS),
    'district': np.random.choice(['Kathmandu', 'Kaski', 'Morang', 'Lalitpur', 'Bhaktapur'], NUM_SHOPS)
})

# Generate synthetic products
categories = ['Beverage', 'Snacks', 'Dairy', 'Household', 'Personal Care']
brands = {
    'Beverage': ['Coca-Cola', 'Pepsi', 'Red Bull', 'Nestle'],
    'Snacks': ['Wai Wai', 'Kurkure', 'Pringles', 'Lays'],
    'Dairy': ['Amul', 'Dairy Milk', 'Yak Cheese', 'Nestle'],
    'Household': ['Surf Excel', 'Vim', 'Harpic', 'Colin'],
    'Personal Care': ['Dove', 'Lux', 'Patanjali', 'Himalaya']
}

products = []
for i in range(1, NUM_PRODUCTS+1):
    category = random.choice(categories)
    brand = random.choice(brands[category])
    products.append({
        'product_id': i,
        'product_name': f"{brand} {category[:3]}{i}",
        'category': category,
        'brand': brand,
        'standard_price': round(random.uniform(10, 500), 2)
    })

products = pd.DataFrame(products)

# Generate synthetic transactions
transactions = []
for _ in range(NUM_TRANSACTIONS):
    shop_id = random.randint(1, NUM_SHOPS)
    product_id = random.randint(1, NUM_PRODUCTS)
    quantity = random.randint(1, 10)
    
    # Get product price with some random variation
    base_price = products.loc[products['product_id'] == product_id, 'standard_price'].values[0]
    selling_price = round(base_price * random.uniform(0.9, 1.1), 2)
    
    # Random date within range
    date = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
    
    transactions.append({
        'shop_id': shop_id,
        'product_id': product_id,
        'transaction_type': 'SALE',
        'quantity': quantity,
        'unit_price': selling_price,
        'total_amount': round(selling_price * quantity, 2),
        'transaction_time': date,
        'payment_method': random.choice(['CASH', 'CARD', 'UPI'])
    })

transactions = pd.DataFrame(transactions)

# Save to CSV
shops.to_csv('shops.csv', index=False)
products.to_csv('products.csv', index=False)
transactions.to_csv('transactions.csv', index=False)