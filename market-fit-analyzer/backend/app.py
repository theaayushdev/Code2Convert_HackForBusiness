import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

from product_performance import (
    prepare_monthly_data, create_features, train_model
)

st.set_page_config(page_title="📈 Retail Sales Predictor", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Retail Product Sales Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

def load_data(transactions_file, products_file, shops_file):
    # Load CSVs
    transactions = pd.read_csv(transactions_file)
    products = pd.read_csv(products_file)
    shops = pd.read_csv(shops_file)
    
    # Merge data: assuming 'product_id' and 'shop_id' common keys
    data = transactions.merge(products, on='product_id', how='left')
    data = data.merge(shops, on='shop_id', how='left')
    return data


def get_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {'mae': mae, 'rmse': rmse}


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


if st.sidebar:
    st.header("📂 Upload CSV Files")
    transactions_file = st.file_uploader("🧾 Transactions CSV", type="csv")
    products_file = st.file_uploader("🛒 Products CSV", type="csv")
    shops_file = st.file_uploader("🏬 Shops CSV", type="csv")
    st.markdown("---")
    st.info("Upload all 3 files to begin analysis.")

if transactions_file and products_file and shops_file:
    with st.spinner("🔄 Processing uploaded data..."):
        data = load_data(transactions_file, products_file, shops_file)
        monthly_data = prepare_monthly_data(data)
        monthly_data = create_features(monthly_data)

        model = train_model(monthly_data)

        # Get feature columns used in model
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
    col1, col2 = st.columns(2)
    col1.metric("MAE", f"{metrics['mae']:.2f}")
    col2.metric("RMSE", f"{metrics['rmse']:.2f}")

    # Charts
    with st.expander("📊 Data Insights & Visualizations", expanded=True):
        # Monthly Sales Trend (sum over all products & shops)
        st.subheader("📈 Monthly Sales Trend (All Products & Shops Combined)")
        monthly_sales = monthly_data.groupby('year_month')['monthly_quantity'].sum().reset_index()
        monthly_sales['month_start'] = monthly_sales['year_month'].dt.to_timestamp()
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.lineplot(data=monthly_sales, x='month_start', y='monthly_quantity', marker='o', ax=ax)
        ax.set_title("Monthly Sales Trend Over Time")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Units Sold")
        st.pyplot(fig)

        # Sales by Shop
        st.subheader("🏬 Total Sales by Shop")
        sales_by_shop = monthly_data.groupby('shop_id')['monthly_quantity'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=sales_by_shop.index, y=sales_by_shop.values, palette="Blues_d", ax=ax)
        ax.set_xlabel("Shop ID")
        ax.set_ylabel("Total Units Sold")
        ax.set_title("Total Sales per Shop")
        st.pyplot(fig)

        # Top Products
        st.subheader("🛍️ Top 10 Best-Selling Products")
        top_products = monthly_data.groupby('product_id')['monthly_quantity'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=top_products.index, y=top_products.values, palette="mako", ax=ax)
        ax.set_xlabel("Total Units Sold")
        ax.set_ylabel("Product ID")
        ax.set_title("Top 10 Products by Total Sales")
        st.pyplot(fig)

        # Sales Heatmap
        st.subheader("📊 Sales Heatmap: Shops vs Months")
        heatmap_data = monthly_data.pivot_table(index='shop_id', columns='year_month',
                                                values='monthly_quantity', aggfunc='sum').fillna(0)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.1, ax=ax)
        ax.set_title("Monthly Sales Volume per Shop")
        ax.set_xlabel("Month")
        ax.set_ylabel("Shop ID")
        st.pyplot(fig)

        # Sales Distribution
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
            prediction, status = predict_next_month(model, feature_columns, monthly_data, product_id, shop_id)
            if status == "Success":
                st.success(f"🟢 Predicted sales for next month: **{prediction} units**")
                # Historical trend plot
                st.subheader("📉 Historical Sales Trend for Selected Product-Shop")
                selected_data = monthly_data[(monthly_data['product_id'] == product_id) & (monthly_data['shop_id'] == shop_id)]
                if not selected_data.empty:
                    fig, ax = plt.subplots(figsize=(10, 4))
                    sns.lineplot(data=selected_data, x='year_month', y='monthly_quantity', marker='o', ax=ax)
                    ax.set_title(f"Sales Trend: Product {product_id} at Shop {shop_id}")
                    ax.set_xlabel("Month")
                    ax.set_ylabel("Units Sold")
                    st.pyplot(fig)
                else:
                    st.info("No historical sales data for this product-shop combination.")
            else:
                st.warning(f"⚠️ {status}")
else:
    st.info("👈 Please upload all three CSV files from the sidebar to begin.")
