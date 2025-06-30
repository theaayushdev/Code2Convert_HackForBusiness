import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

from product_performance import (
    prepare_monthly_data, create_features, train_model
)

st.set_page_config(page_title="📈 Retail Sales Predictor", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Retail Product Sales Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

def load_data(transactions_file, products_file, shops_file):
    transactions = pd.read_csv(transactions_file)
    products = pd.read_csv(products_file)
    shops = pd.read_csv(shops_file)

    # Clean IDs for consistency
    transactions['product_id'] = transactions['product_id'].astype(str).str.strip()
    products['product_id'] = products['product_id'].astype(str).str.strip()
    transactions['shop_id'] = transactions['shop_id'].astype(str).str.strip()
    shops['shop_id'] = shops['shop_id'].astype(str).str.strip()

    # Merge
    data = transactions.merge(products, on='product_id', how='left')
    data = data.merge(shops, on='shop_id', how='left')

    return data, products, shops

def get_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return {'mae': mae, 'rmse': rmse, 'r2': r2}

def get_all_predictions(model, feature_columns, data):
    data['predicted_quantity'] = model.predict(data[feature_columns])
    return data[['product_id', 'shop_id', 'year_month', 'monthly_quantity', 'predicted_quantity']]

def predict_next_month(model, feature_columns, data, product_id, shop_id):
    subset = data[(data['product_id'] == product_id) & (data['shop_id'] == shop_id)]
    if subset.empty:
        return None, "No data for this product-shop"

    latest_row = subset.sort_values('year_month').iloc[-1]
    X = latest_row[feature_columns].values.reshape(1, -1)
    prediction = model.predict(X)[0]
    return round(prediction, 2), "Success"

# Sidebar: Upload files
if st.sidebar:
    st.header("📂 Upload CSV Files")
    transactions_file = st.file_uploader("🧾 Transactions CSV", type="csv")
    products_file = st.file_uploader("🛒 Products CSV", type="csv")
    shops_file = st.file_uploader("🏬 Shops CSV", type="csv")
    st.markdown("---")
    st.info("Upload all 3 files to begin analysis.")

# Once files are uploaded
if transactions_file and products_file and shops_file:
    with st.spinner("🔄 Processing uploaded data..."):
        data, products, shops = load_data(transactions_file, products_file, shops_file)
        monthly_data = prepare_monthly_data(data)
        monthly_data = create_features(monthly_data)

        model = train_model(monthly_data)

        feature_columns = [
            'last_month_qty', 'last_2_months_qty', 'last_3_months_qty',
            'avg_last_3_months', 'trend', 'price_difference',
            'is_holiday_month', 'is_summer', 'category_code', 'city_code'
        ]

        y_true = monthly_data['monthly_quantity']
        y_pred = model.predict(monthly_data[feature_columns])
        metrics = get_metrics(y_true, y_pred)

    st.success("✅ Model trained successfully!")

    # Model Metrics
    st.subheader("📐 Model Performance Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"{metrics['mae']:.2f}")
    col2.metric("RMSE", f"{metrics['rmse']:.2f}")
    col3.metric("R²", f"{metrics['r2']:.2f}")
    st.markdown("---")

    # Charts & Insights
    with st.expander("📊 Data Insights & Visualizations", expanded=True):
        st.subheader("📈 Monthly Sales Trend (All Products & Shops Combined)")
        monthly_sales = monthly_data.groupby('year_month')['monthly_quantity'].sum().reset_index()
        monthly_sales['month_start'] = monthly_sales['year_month'].dt.to_timestamp()
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=monthly_sales, x='month_start', y='monthly_quantity', marker='o', ax=ax)
        ax.set_title("Monthly Sales Trend Over Time")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Units Sold")
        st.pyplot(fig)

        st.subheader("🏬 Total Sales by Shop")
        sales_by_shop = monthly_data.groupby('shop_id')['monthly_quantity'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=sales_by_shop.index, y=sales_by_shop.values, palette="Blues_d", ax=ax)
        ax.set_xlabel("Shop ID")
        ax.set_xticklabels(sales_by_shop.index, rotation=45, fontsize=6)
        ax.set_ylabel("Total Units Sold")
        ax.set_title("Total Sales per Shop")
        st.pyplot(fig)

        st.subheader("🛍️ Top 10 Best-Selling Products")
        top_products = monthly_data.groupby('product_id')['monthly_quantity'].sum().sort_values(ascending=False).head(10)
        top_products_df = top_products.reset_index().merge(products[['product_id', 'product_name']], on='product_id', how='left')
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='monthly_quantity', y='product_name', data=top_products_df, palette="mako", ax=ax)
        ax.set_xlabel("Total Units Sold")
        ax.set_ylabel("Product Name")
        ax.set_title("Top 10 Products by Total Sales")
        st.pyplot(fig)

        st.subheader("📊 Sales Heatmap: Shops vs Months")
        heatmap_data = monthly_data.pivot_table(index='shop_id', columns='year_month',
                                                values='monthly_quantity', aggfunc='sum').fillna(0)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.1, ax=ax)
        ax.set_title("Monthly Sales Volume per Shop")
        ax.set_xlabel("Month")
        ax.set_ylabel("Shop ID")
        st.pyplot(fig)

        st.subheader("📦 Distribution of Monthly Sales")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(monthly_data['monthly_quantity'], bins=50, kde=True, color='skyblue', ax=ax)
        ax.set_title("Distribution of Monthly Sales Quantity")
        ax.set_xlabel("Monthly Sales Quantity")
        st.pyplot(fig)

    # Feature Importance
    st.subheader("📊 Feature Importance (Top Features Used by Model)")
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': feature_columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=feature_importance_df.head(10), x='Importance', y='Feature', palette="viridis", ax=ax)
    ax.set_title("Top 10 Important Features for Prediction")
    st.pyplot(fig)

    # Show All Predictions
    with st.expander("📄 Show All Predictions", expanded=False):
        if st.checkbox("🔍 View All Forecasted Sales"):
            predictions = get_all_predictions(model, feature_columns, monthly_data)
            st.dataframe(predictions)
            csv = predictions.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Predictions as CSV", csv, "predictions.csv", "text/csv")

    # Predict for Specific Product-Shop
    st.markdown("---")
    st.subheader("🎯 Predict Sales for Specific Product-Shop")
    col1, col2 = st.columns(2)
    product_id = col1.selectbox("🔢 Select Product ID", monthly_data['product_id'].unique())
    shop_id = col2.selectbox("🏬 Select Shop ID", monthly_data['shop_id'].unique())

    if st.button("📈 Predict Next Month's Sales"):
        with st.spinner("⏳ Generating prediction..."):
            # First check if data exists for this product-shop pair
            historical_check = monthly_data[
                (monthly_data['product_id'] == product_id) & 
                (monthly_data['shop_id'] == shop_id)
            ]
            
            if not historical_check.empty:
                # Data exists - proceed with prediction
                prediction, status = predict_next_month(model, feature_columns, monthly_data, product_id, shop_id)
                
                if status == "Success":
                    st.success(f"🟢 Predicted sales for next month: **{prediction:.0f} units**")
                    
                    # Display historical trend
                    st.subheader("📉 Historical Sales Trend")
                    fig, ax = plt.subplots(figsize=(10, 4))
                    import matplotlib.dates as mdates
                    

                    # Convert Period to Timestamp (FIX for the TypeError)
                    if pd.api.types.is_period_dtype(historical_check['year_month']):
                        historical_check['year_month'] = historical_check['year_month'].dt.to_timestamp()
                    else:
                        historical_check['year_month'] = pd.to_datetime(historical_check['year_month'], format='%Y-%m')

                    # Ensure numeric data
                    historical_check['monthly_quantity'] = pd.to_numeric(historical_check['monthly_quantity'])

                    # Sort by date
                    historical_check = historical_check.sort_values('year_month')

                    # Create plot
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.lineplot(
                        data=historical_check,
                        x='year_month',
                        y='monthly_quantity',
                        marker='o',
                        ax=ax
                    )

                    # Formatting
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # "May 2023"
                    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
                    plt.xticks(rotation=45)
                    ax.set_title(f"Sales Trend: Product {product_id} at Shop {shop_id}")
                    ax.axhline(prediction, color='r', linestyle='--', label=f'Prediction: {prediction:.0f}')

                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Show additional stats
                    with st.expander("📊 Detailed Historical Data"):
                        st.dataframe(historical_check.sort_values('year_month', ascending=False))
                else:
                    st.error(f"🔴 Prediction failed: {status}")
            
            else:
                # No historical data exists
                st.warning(f"⚠️ No historical sales data found for Product {product_id} at Shop {shop_id}")
                
                # Show alternatives
                st.subheader("🔍 Try these alternatives:")
                
                # 1. Similar products at this shop
                similar_at_shop = monthly_data[
                    (monthly_data['shop_id'] == shop_id)
                ].groupby('product_id')['monthly_quantity'].sum().nlargest(5)
                
                # 2. This product at other shops
                product_at_other_shops = monthly_data[
                    (monthly_data['product_id'] == product_id)
                ].groupby('shop_id')['monthly_quantity'].sum().nlargest(5)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Top products at this shop:**")
                    st.dataframe(similar_at_shop)
                    
                with col2:
                    st.write(f"**Product {product_id} at other shops:**")
                    st.dataframe(product_at_other_shops)