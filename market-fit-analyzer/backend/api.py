from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
import traceback
import logging
import os
import glob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Global variables for model and data
model_metadata = None
transactions_df = None
products_df = None
shops_df = None
predictions_df = None

def load_latest_predictions():
    """Load the latest sales predictions CSV file"""
    global predictions_df
    
    try:
        # Find the latest predictions file
        prediction_files = glob.glob('sales_predictions.csv')
        if not prediction_files:
            logger.warning("No prediction files found")
            return False
        
        # Get the most recent file
        latest_file = max(prediction_files, key=os.path.getctime)
        predictions_df = pd.read_csv(latest_file)
        
        logger.info(f"Loaded predictions from: {latest_file}")
        logger.info(f"Predictions shape: {predictions_df.shape}")
        
        # Display column names for debugging
        logger.info(f"Prediction columns: {list(predictions_df.columns)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading predictions: {e}")
        return False

def load_model_and_data():
    """Load model and data with comprehensive error handling"""
    global model_metadata, transactions_df, products_df, shops_df
    
    try:
        # Load model metadata (optional - might not exist)
        try:
            with open('product_performance_model_complete.pkl', 'rb') as f:
                model_metadata = pickle.load(f)
            logger.info("Model loaded successfully")
        except FileNotFoundError:
            logger.warning("Model file not found - will work with predictions only")
            model_metadata = None
        
        # Load data files
        try:
            transactions_df = pd.read_csv('transactions.csv')
            logger.info(f"Loaded {len(transactions_df)} transactions")
        except FileNotFoundError:
            logger.warning("transactions.csv not found")
            transactions_df = None
        
        try:
            products_df = pd.read_csv('products.csv')
            logger.info(f"Loaded {len(products_df)} products")
        except FileNotFoundError:
            logger.warning("products.csv not found")
            products_df = None
        
        try:
            shops_df = pd.read_csv('shops.csv')
            logger.info(f"Loaded {len(shops_df)} shops")
        except FileNotFoundError:
            logger.warning("shops.csv not found")
            shops_df = None
        
        # Preprocess transaction data if available
        if transactions_df is not None:
            transactions_df['transaction_time'] = pd.to_datetime(transactions_df['transaction_time'])
            transactions_df['month'] = transactions_df['transaction_time'].dt.month
            transactions_df['day_of_week'] = transactions_df['transaction_time'].dt.dayofweek
            transactions_df['hour'] = transactions_df['transaction_time'].dt.hour
        
        # Load predictions
        predictions_loaded = load_latest_predictions()
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return False

def get_product_prediction(product_id):
    """Get prediction for a specific product from CSV"""
    try:
        if predictions_df is None:
            return None, "No predictions data available"
        
        # Find the product in predictions
        product_pred = predictions_df[predictions_df['product_id'] == product_id]
        if product_pred.empty:
            return None, f"No prediction found for product {product_id}"
        
        # Get the prediction data
        pred_row = product_pred.iloc[0]
        
        # Extract prediction value - adjust column name based on your CSV structure
        prediction_columns = [col for col in predictions_df.columns if 'prediction' in col.lower() or 'forecast' in col.lower()]
        
        if prediction_columns:
            prediction_value = pred_row[prediction_columns[0]]
        else:
            # Fallback - look for numeric columns that might contain predictions
            numeric_cols = predictions_df.select_dtypes(include=[np.number]).columns
            non_id_cols = [col for col in numeric_cols if 'id' not in col.lower()]
            if non_id_cols:
                prediction_value = pred_row[non_id_cols[0]]
            else:
                return None, "Could not identify prediction column"
        
        return float(prediction_value), None
        
    except Exception as e:
        logger.error(f"Error getting prediction for product {product_id}: {e}")
        return None, str(e)

def create_product_features(product_id):
    """Create features for a specific product from historical data"""
    try:
        if transactions_df is None:
            return None, "No transaction data available"
        
        # Filter sales transactions for this product
        product_sales = transactions_df[
            (transactions_df['product_id'] == product_id) & 
            (transactions_df['transaction_type'] == 'SALE')
        ].copy()
        
        if product_sales.empty:
            return None, "No sales data found for this product"
        
        # Create aggregated features
        features = {}
        
        # Basic sales metrics
        features['total_units'] = product_sales['quantity'].sum()
        features['avg_quantity'] = product_sales['quantity'].mean()
        features['std_quantity'] = product_sales['quantity'].std() if len(product_sales) > 1 else 0
        features['sales_count'] = len(product_sales)
        features['total_revenue'] = product_sales['total_amount'].sum()
        features['avg_revenue'] = product_sales['total_amount'].mean()
        features['std_revenue'] = product_sales['total_amount'].std() if len(product_sales) > 1 else 0
        features['avg_price'] = product_sales['unit_price'].mean()
        features['std_price'] = product_sales['unit_price'].std() if len(product_sales) > 1 else 0
        
        # Behavioral features
        features['avg_day_preference'] = product_sales['day_of_week'].mean()
        features['avg_hour_preference'] = product_sales['hour'].mean()
        features['shop_diversity'] = product_sales['shop_id'].nunique()
        
        # Most preferred payment method
        payment_counts = product_sales['payment_method'].value_counts()
        features['preferred_payment'] = payment_counts.index[0] if len(payment_counts) > 0 else 'CASH'
        
        # Monthly sales (fill missing months with 0)
        monthly_sales = product_sales.groupby('month')['quantity'].sum()
        for month in range(1, 13):
            features[f'month_{month}_sales'] = monthly_sales.get(month, 0)
        
        return features, None
        
    except Exception as e:
        logger.error(f"Error creating features for product {product_id}: {e}")
        return None, str(e)

# Initialize on startup
if not load_model_and_data():
    logger.error("Failed to load data. Some features may not be available.")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_metadata is not None,
        'transactions_loaded': transactions_df is not None,
        'products_loaded': products_df is not None,
        'predictions_loaded': predictions_df is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/predict_performance', methods=['POST'])
def predict_performance():
    """Main prediction endpoint using CSV predictions"""
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        
        if product_id is None:
            return jsonify({'error': 'Missing product_id'}), 400

        # Get prediction from CSV
        prediction, err = get_product_prediction(product_id)
        if prediction is None:
            return jsonify({'error': err or 'Prediction not available'}), 404

        # Get historical features if available
        historical_data = {}
        if transactions_df is not None:
            features_dict, _ = create_product_features(product_id)
            if features_dict:
                historical_data = {
                    'total_sales': int(features_dict.get('sales_count', 0)),
                    'total_units_sold': int(features_dict.get('total_units', 0)),
                    'total_revenue': float(features_dict.get('total_revenue', 0.0)),
                    'shop_diversity': int(features_dict.get('shop_diversity', 0))
                }

        response = {
            'predicted_next_month_sales': float(prediction),
            'confidence_score': 0.85,  # You can enhance this based on your model
            'historical_data': historical_data,
            'prediction_source': 'csv_file'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Internal server error occurred'}), 500

@app.route('/product_analytics/<int:product_id>', methods=['GET'])
def get_product_analytics(product_id):
    """Get detailed analytics for a product"""
    try:
        # Get prediction from CSV
        prediction, pred_err = get_product_prediction(product_id)
        
        # Initialize response
        analytics = {
            'product_id': product_id,
            'predicted_sales': float(prediction) if prediction is not None else None,
            'prediction_available': prediction is not None
        }
        
        # Add product info if available
        if products_df is not None and product_id in products_df['product_id'].values:
            product_info = products_df[products_df['product_id'] == product_id].iloc[0]
            analytics.update({
                'product_name': product_info.get('product_name', f'Product {product_id}'),
                'category': product_info.get('category', 'Unknown')
            })
        else:
            analytics.update({
                'product_name': f'Product {product_id}',
                'category': 'Unknown'
            })
        
        # Add historical data if available
        if transactions_df is not None:
            product_sales = transactions_df[
                (transactions_df['product_id'] == product_id) & 
                (transactions_df['transaction_type'] == 'SALE')
            ]
            
            if not product_sales.empty:
                monthly_sales = product_sales.groupby('month').agg({
                    'quantity': 'sum',
                    'total_amount': 'sum'
                }).to_dict('index')
                
                analytics.update({
                    'total_sales_count': len(product_sales),
                    'total_units_sold': int(product_sales['quantity'].sum()),
                    'total_revenue': round(product_sales['total_amount'].sum(), 2),
                    'avg_unit_price': round(product_sales['unit_price'].mean(), 2),
                    'shops_selling': int(product_sales['shop_id'].nunique()),
                    'monthly_breakdown': {
                        str(month): {
                            'units': int(data['quantity']),
                            'revenue': round(data['total_amount'], 2)
                        } for month, data in monthly_sales.items()
                    },
                    'payment_methods': product_sales['payment_method'].value_counts().to_dict(),
                    'peak_hour': int(product_sales['hour'].mode().iloc[0]) if not product_sales['hour'].mode().empty else 0
                })
        
        return jsonify(analytics)
        
    except Exception as e:
        logger.error(f"Analytics error for product {product_id}: {e}")
        return jsonify({'error': 'Failed to generate analytics'}), 500

@app.route('/products', methods=['GET'])
def get_products():
    """Get list of all products with prediction availability"""
    try:
        product_list = []
        
        # If we have predictions CSV, use it as the primary source
        if predictions_df is not None:
            for _, pred_row in predictions_df.iterrows():
                product_id = pred_row['product_id']
                
                product_info = {
                    'product_id': int(product_id),
                    'has_prediction_data': True
                }
                
                # Add product details if available
                if products_df is not None and product_id in products_df['product_id'].values:
                    product_data = products_df[products_df['product_id'] == product_id].iloc[0]
                    product_info.update({
                        'product_name': product_data.get('product_name', f'Product {product_id}'),
                        'category': product_data.get('category', 'Unknown')
                    })
                else:
                    product_info.update({
                        'product_name': f'Product {product_id}',
                        'category': 'Unknown'
                    })
                
                # Add sales count if transaction data available
                if transactions_df is not None:
                    sales_count = len(transactions_df[
                        (transactions_df['product_id'] == product_id) & 
                        (transactions_df['transaction_type'] == 'SALE')
                    ])
                    product_info['sales_count'] = sales_count
                
                product_list.append(product_info)
        
        # Fallback to products.csv if no predictions
        elif products_df is not None:
            for _, product in products_df.iterrows():
                product_id = product['product_id']
                
                sales_count = 0
                if transactions_df is not None:
                    sales_count = len(transactions_df[
                        (transactions_df['product_id'] == product_id) & 
                        (transactions_df['transaction_type'] == 'SALE')
                    ])
                
                product_list.append({
                    'product_id': int(product_id),
                    'product_name': product.get('product_name', f'Product {product_id}'),
                    'category': product.get('category', 'Unknown'),
                    'sales_count': sales_count,
                    'has_prediction_data': False
                })
        
        return jsonify({'products': product_list})
        
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        return jsonify({'error': 'Failed to fetch products'}), 500

@app.route('/predictions', methods=['GET'])
def get_all_predictions():
    """Get all predictions from CSV"""
    try:
        if predictions_df is None:
            return jsonify({'error': 'No predictions data available'}), 404
        
        # Convert predictions to JSON format
        predictions_list = []
        for _, row in predictions_df.iterrows():
            pred_dict = row.to_dict()
            
            # Convert numpy types to native Python types
            for key, value in pred_dict.items():
                if isinstance(value, (np.integer, np.int64)):
                    pred_dict[key] = int(value)
                elif isinstance(value, (np.floating, np.float64)):
                    pred_dict[key] = float(value)
            
            predictions_list.append(pred_dict)
        
        return jsonify({
            'predictions': predictions_list,
            'total_count': len(predictions_list),
            'columns': list(predictions_df.columns)
        })
        
    except Exception as e:
        logger.error(f"Error getting all predictions: {e}")
        return jsonify({'error': 'Failed to fetch predictions'}), 500

@app.route('/reload_predictions', methods=['POST'])
def reload_predictions():
    """Reload predictions from the latest CSV file"""
    try:
        success = load_latest_predictions()
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Predictions reloaded successfully',
                'prediction_count': len(predictions_df) if predictions_df is not None else 0
            })
        else:
            return jsonify({'error': 'Failed to reload predictions'}), 500
            
    except Exception as e:
        logger.error(f"Error reloading predictions: {e}")
        return jsonify({'error': 'Failed to reload predictions'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Enhanced Product Performance API...")
    print("Data Status:")
    print(f"  - Model loaded: {model_metadata is not None}")
    print(f"  - Transactions loaded: {transactions_df is not None}")
    print(f"  - Products loaded: {products_df is not None}")
    print(f"  - Predictions loaded: {predictions_df is not None}")
    
    if predictions_df is not None:
        print(f"  - Predictions count: {len(predictions_df)}")
        print(f"  - Prediction columns: {list(predictions_df.columns)}")
    
    print("\nAvailable endpoints:")
    print("  - POST /predict_performance")
    print("  - GET /product_analytics/<product_id>")
    print("  - GET /products")
    print("  - GET /predictions")
    print("  - POST /reload_predictions")
    print("  - GET /health")
    
    app.run(debug=True, host='0.0.0.0', port=5001)