import random
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# Define data pools for random generation
nepali_first_names = [
    'Ram', 'Shyam', 'Hari', 'Krishna', 'Gopal', 'Bishnu', 'Shiva', 'Ganesh',
    'Sita', 'Gita', 'Maya', 'Kamala', 'Radha', 'Laxmi', 'Saraswoti', 'Parvati',
    'Raj', 'Ravi', 'Sunil', 'Anil', 'Manoj', 'Santosh', 'Prakash', 'Dinesh',
    'Sunita', 'Anita', 'Geeta', 'Nita', 'Rita', 'Mina', 'Tina', 'Dina',
    'Tek', 'Dil', 'Man', 'Bir', 'Jit', 'Dev', 'Nara', 'Bhupal',
    'Indira', 'Sarita', 'Kavita', 'Babita', 'Sangita', 'Archana', 'Kalpana', 'Rashmi',
    'Bijay', 'Ujjwal', 'Deepak', 'Sanjay', 'Mahesh', 'Naresh', 'Lokesh', 'Rakesh',
    'Bindu', 'Shanti', 'Durga', 'Kiran', 'Puspa', 'Sabita', 'Urmila', 'Sushma'
]

nepali_last_names = [
    'Sharma', 'Shrestha', 'Tamang', 'Gurung', 'Magar', 'Rai', 'Limbu', 'Sherpa',
    'Thapa', 'Khadka', 'Adhikari', 'Poudel', 'Karki', 'Acharya', 'Bhattarai', 'Regmi',
    'Neupane', 'Ghimire', 'Panthi', 'Koirala', 'Maharjan', 'Shakya', 'Manandhar', 'Joshi',
    'Pradhan', 'Karmacharya', 'Dangol', 'Singh', 'Tharu', 'Chaudhary', 'Yadav', 'Mandal',
    'KC', 'BK', 'Bohora', 'Oli', 'Pandey', 'Mishra', 'Tiwari', 'Upadhyay',
    'Basnet', 'Kafle', 'Bhandari', 'Dahal', 'Rijal', 'Silwal', 'Parajuli', 'Subedi'
]

shop_prefixes = [
    'Sunrise', 'Modern', 'Quick', 'City', 'Valley', 'Fresh', 'Local', 'Metro',
    'Corner', 'Heritage', 'Traditional', 'Smart', 'Digital', 'Express', 'Super',
    'Village', 'Mountain', 'Hill', 'River', 'New Age', 'Tech', 'Future', 'Prime',
    'Elite', 'Royal', 'Golden', 'Silver', 'Diamond', 'Pearl', 'Star', 'Lucky',
    'Happy', 'Bright', 'Rainbow', 'Sunshine', 'Moonlight', 'Crystal', 'Global',
    'Universal', 'Central', 'Grand', 'Supreme', 'Ultimate', 'Perfect', 'Quality',
    'Best', 'Top', 'Choice', 'Select', 'Premium', 'Classic', 'Popular', 'Famous'
]

shop_suffixes = [
    'Store', 'Mart', 'Shop', 'Bazaar', 'Market', 'Center', 'Plaza', 'Hub',
    'Point', 'Corner', 'Junction', 'Emporium', 'Outlet', 'Gallery', 'World',
    'Palace', 'House', 'Zone', 'Station', 'Complex', 'Mall', 'Supermarket',
    'General Store', 'Trading', 'Enterprise', 'Collection', 'Suppliers'
]

# Nepal districts and major cities
nepal_locations = [
    ('Kathmandu', 'Kathmandu'),
    ('Lalitpur', 'Lalitpur'),
    ('Bhaktapur', 'Bhaktapur'),
    ('Pokhara', 'Kaski'),
    ('Biratnagar', 'Morang'),
    ('Birgunj', 'Parsa'),
    ('Dharan', 'Sunsari'),
    ('Butwal', 'Rupandehi'),
    ('Nepalgunj', 'Banke'),
    ('Hetauda', 'Makwanpur'),
    ('Janakpur', 'Dhanusha'),
    ('Bharatpur', 'Chitwan'),
    ('Itahari', 'Sunsari'),
    ('Gorkha', 'Gorkha'),
    ('Baglung', 'Baglung'),
    ('Tansen', 'Palpa'),
    ('Dhulikhel', 'Kavrepalanchok'),
    ('Banepa', 'Kavrepalanchok'),
    ('Kirtipur', 'Kathmandu'),
    ('Bhairahawa', 'Rupandehi'),
    ('Damak', 'Jhapa'),
    ('Triyuga', 'Udayapur'),
    ('Tulsipur', 'Dang'),
    ('Gulariya', 'Bardiya'),
    ('Tikapur', 'Kailali'),
    ('Dhangadhi', 'Kailali'),
    ('Mahendranagar', 'Kanchanpur'),
    ('Dipayal', 'Doti'),
    ('Silgadhi', 'Doti'),
    ('Mangalsen', 'Achham'),
    ('Chainpur', 'Bajhang'),
    ('Martadi', 'Bajura'),
    ('Gamgadhi', 'Mugu'),
    ('Simikot', 'Humla'),
    ('Jumla', 'Jumla'),
    ('Dunai', 'Dolpa'),
    ('Jomsom', 'Mustang'),
    ('Chame', 'Manang'),
    ('Besisahar', 'Lamjung'),
    ('Damauli', 'Tanahun'),
    ('Kusma', 'Parbat'),
    ('Beni', 'Myagdi'),
    ('Lete', 'Mustang'),
    ('Syangja', 'Syangja'),
    ('Waling', 'Syangja'),
    ('Bhimad', 'Tanahun'),
    ('Bandipur', 'Tanahun'),
    ('Gorkha', 'Gorkha'),
    ('Arughat', 'Gorkha')
]

def generate_shop_data(num_records=1000):
    """Generate random shop data matching SHOP table structure exactly"""
    
    shops = []
    
    for i in range(num_records):
        # Generate shop name
        shop_name = f"{random.choice(shop_prefixes)} {random.choice(shop_suffixes)}"
        
        # Generate owner name
        first_name = random.choice(nepali_first_names)
        last_name = random.choice(nepali_last_names)
        if random.random() < 0.3:  # 30% chance of middle name
            middle_name = random.choice(['Bahadur', 'Prasad', 'Kumar', 'Devi', 'Maya', 'Lal'])
            owner_name = f"{first_name} {middle_name} {last_name}"
        else:
            owner_name = f"{first_name} {last_name}"
        
        # Generate phone number (Nepal format)
        phone = f"98{random.randint(40000000, 49999999)}"
        
        # Generate email
        email_prefix = first_name.lower() + "." + shop_name.split()[0].lower()
        email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'email.com']
        email = f"{email_prefix}{random.randint(1, 999)}@{random.choice(email_domains)}"
        
        # Generate location
        city, district = random.choice(nepal_locations)
        ward = random.randint(1, 35)
        area_names = ['Chowk', 'Tole', 'Bazar', 'Road', 'Marg', 'Galli', 'Line', 'Path']
        area = f"{random.choice(['New', 'Old', 'Main', 'Central', 'North', 'South', 'East', 'West'])}{random.choice(area_names)}"
        address = f"{area}-{ward}, {city}"
        
        # Generate created_at (shop registration date)
        years_back = random.randint(1, 15)  # 1-15 years ago
        days_back = years_back * 365 + random.randint(0, 365)
        created_at = datetime.now() - timedelta(days=days_back)
        created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S')
        
        # Generate last_sync
        is_active = random.choice([True, True, True, True, False])  # 80% active
        
        if is_active:
            # Active shops sync recently (0-30 days ago)
            sync_days_ago = random.randint(0, 30)
            last_sync_dt = datetime.now() - timedelta(days=sync_days_ago, 
                                                     hours=random.randint(0, 23),
                                                     minutes=random.randint(0, 59))
            last_sync = last_sync_dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # Inactive shops: 30% never synced (NULL), 70% old sync
            if random.random() < 0.3:
                last_sync = None
            else:
                sync_days_ago = random.randint(90, 500)  # 3 months to 1.5 years ago
                last_sync_dt = datetime.now() - timedelta(days=sync_days_ago,
                                                         hours=random.randint(0, 23),
                                                         minutes=random.randint(0, 59))
                last_sync = last_sync_dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Create shop record matching exact SHOP table structure
        shop = {
            'shop_name': shop_name,
            'owner_name': owner_name,
            'phone': phone,
            'email': email,
            'address': address,
            'city': city,
            'district': district,
            'created_at': created_at_str,
            'last_sync': last_sync,
            'is_active': is_active
        }
        
        shops.append(shop)
    
    return shops

def generate_sql_insert_statements(shops):
    """Generate SQL INSERT statements for SHOP table"""
    
    sql_statements = []
    sql_statements.append("""-- Generated shop data for SHOP table
-- Total records: """ + str(len(shops)) + """
INSERT INTO SHOP (
    shop_name, owner_name, phone, email, address, city, district, 
    created_at, last_sync, is_active
) VALUES""")
    
    for i, shop in enumerate(shops):
        # Handle NULL last_sync
        last_sync_val = 'NULL' if shop['last_sync'] is None else f"'{shop['last_sync']}'"
        
        values = f"""(
    '{shop['shop_name']}', '{shop['owner_name']}', '{shop['phone']}', 
    '{shop['email']}', '{shop['address']}', '{shop['city']}', 
    '{shop['district']}', '{shop['created_at']}', {last_sync_val}, {shop['is_active']}
)"""
        
        if i < len(shops) - 1:
            values += ","
        else:
            values += ";"
            
        sql_statements.append(values)
    
    return "\n".join(sql_statements)

# Generate the data
print("Generating 1000 shop records for SHOP table...")
shops = generate_shop_data(1000)

# Create DataFrame
df = pd.DataFrame(shops)

# Display sample data
print(f"\n✅ Generated {len(shops)} shop records")
print("\nSample of generated data:")
print(df.head())

print(f"\nData shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Basic statistics
print(f"\n📊 Data Summary:")
print(f"- Total shops: {len(shops)}")
print(f"- Active shops: {df['is_active'].sum()}")
print(f"- Inactive shops: {len(df) - df['is_active'].sum()}")
print(f"- Unique cities: {df['city'].nunique()}")
print(f"- Unique districts: {df['district'].nunique()}")
print(f"- Shops with NULL last_sync: {df['last_sync'].isna().sum()}")

# Generate SQL insert statements
print("\nGenerating SQL INSERT statements...")
sql_statements = generate_sql_insert_statements(shops)

# Save SQL file
with open('shop_data_1000.sql', 'w', encoding='utf-8') as f:
    f.write(sql_statements)

print("✅ SQL file saved as 'shop_data_1000.sql'")

# Save as CSV
df.to_csv('shop_data_1000.csv', index=False)
print("✅ CSV file saved as 'shop_data_1000.csv'")

print(f"\n🎯 Ready to use:")
print(f"1. Execute 'shop_data_1000.sql' in your MySQL database")
print(f"2. Use 'shop_data_1000.csv' for data analysis")

print(f"\n📋 Table structure matched:")
print(f"- shop_id: AUTO_INCREMENT (handled by database)")
print(f"- shop_name: VARCHAR(255) NOT NULL ✓")
print(f"- owner_name: VARCHAR(255) NOT NULL ✓")
print(f"- phone: VARCHAR(20) ✓")
print(f"- email: VARCHAR(255) ✓")
print(f"- address: TEXT ✓")
print(f"- city: VARCHAR(100) NOT NULL ✓")
print(f"- district: VARCHAR(100) NOT NULL ✓")
print(f"- created_at: DATETIME ✓")
print(f"- last_sync: DATETIME (with NULLs) ✓")
print(f"- is_active: BOOLEAN ✓")