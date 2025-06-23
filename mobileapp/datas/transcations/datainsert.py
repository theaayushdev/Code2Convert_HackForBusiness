import pandas as pd
from sqlalchemy import create_engine

# Load your CSV file
df = pd.read_csv('transactions.csv')

# For SQLite

engine = create_engine('mysql+pymysql://root:root@localhost/product_sales_report')

# Insert data into table called 'your_table_name'
df.to_sql('transcations', con=engine, if_exists='append', index=False)
