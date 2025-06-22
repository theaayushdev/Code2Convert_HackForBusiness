import 'package:flutter/material.dart';
import 'screens/dashboard_page.dart';

void main() {
  runApp(NepalShopApp());
}

class NepalShopApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Nepal Shop Manager',
      theme: ThemeData(
        primarySwatch: Colors.green,
        primaryColor: Color(0xFF1E88E5),
        fontFamily: 'Roboto',
      ),
      home: ShopHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class Product {
  final String name;
  final String category;
  final double price;
  final String unit;
  int quantity;

  Product({
    required this.name,
    required this.category,
    required this.price,
    required this.unit,
    this.quantity = 0,
  });
}

class SaleRecord {
  final String productName;
  final DateTime time;
  final int quantity;
  final double totalAmount;
  final String type; // 'buy' or 'sell'

  SaleRecord({
    required this.productName,
    required this.time,
    required this.quantity,
    required this.totalAmount,
    required this.type,
  });
}

class ShopHomePage extends StatefulWidget {
  @override
  _ShopHomePageState createState() => _ShopHomePageState();
}

class _ShopHomePageState extends State<ShopHomePage> with TickerProviderStateMixin {
  final TextEditingController _searchController = TextEditingController();
  String _selectedCategory = 'All';
  List<Product> _filteredProducts = [];
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;

  final List<Product> _products = [
    // Electronics
    Product(name: 'Samsung Galaxy Phone', category: 'Electronics', price: 85000, unit: 'piece'),
    Product(name: 'Sony Headphones', category: 'Electronics', price: 12000, unit: 'piece'),
    Product(name: 'Laptop Charger', category: 'Electronics', price: 3500, unit: 'piece'),
    Product(name: 'Power Bank', category: 'Electronics', price: 2800, unit: 'piece'),
    Product(name: 'LED TV', category: 'Electronics', price: 65000, unit: 'piece'),
    Product(name: 'Bluetooth Speaker', category: 'Electronics', price: 4500, unit: 'piece'),
    Product(name: 'Mobile Cover', category: 'Electronics', price: 350, unit: 'piece'),
    Product(name: 'Memory Card', category: 'Electronics', price: 1200, unit: 'piece'),
    // Food Items
    Product(name: 'Basmati Rice', category: 'Food', price: 180, unit: 'kg'),
    Product(name: 'Dal (Lentils)', category: 'Food', price: 150, unit: 'kg'),
    Product(name: 'Chicken', category: 'Food', price: 650, unit: 'kg'),
    Product(name: 'Achar (Pickle)', category: 'Food', price: 280, unit: 'bottle'),
    Product(name: 'Nepali Tea', category: 'Food', price: 45, unit: 'packet'),
    Product(name: 'Ghee', category: 'Food', price: 1200, unit: 'liter'),
    Product(name: 'Honey', category: 'Food', price: 850, unit: 'bottle'),
    Product(name: 'Mustard Oil', category: 'Food', price: 320, unit: 'liter'),
    Product(name: 'Sel Roti Mix', category: 'Food', price: 125, unit: 'packet'),
    Product(name: 'Gundruk', category: 'Food', price: 95, unit: 'packet'),
    // Clothing
    Product(name: 'Dhaka Topi', category: 'Clothing', price: 850, unit: 'piece'),
    Product(name: 'Kurta Suruwal', category: 'Clothing', price: 2500, unit: 'set'),
    Product(name: 'Saree', category: 'Clothing', price: 3200, unit: 'piece'),
    Product(name: 'Pashmina Shawl', category: 'Clothing', price: 1800, unit: 'piece'),
    Product(name: 'T-Shirt', category: 'Clothing', price: 750, unit: 'piece'),
    Product(name: 'Jeans', category: 'Clothing', price: 1950, unit: 'piece'),
    Product(name: 'Traditional Blouse', category: 'Clothing', price: 1200, unit: 'piece'),
    Product(name: 'Cholo (Vest)', category: 'Clothing', price: 950, unit: 'piece'),
  ];

  final List<String> _categories = ['All', 'Electronics', 'Food', 'Clothing'];
  final List<SaleRecord> _sales = [];

  @override
  void initState() {
    super.initState();
    _filteredProducts = _products;
    _animationController = AnimationController(
      duration: Duration(milliseconds: 300),
      vsync: this,
    );
    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(_animationController);
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _filterProducts() {
    setState(() {
      _filteredProducts = _products.where((product) {
        final matchesSearch = product.name.toLowerCase().contains(_searchController.text.toLowerCase());
        final matchesCategory = _selectedCategory == 'All' || product.category == _selectedCategory;
        return matchesSearch && matchesCategory;
      }).toList();
    });
  }

  void _buyProduct(Product product) {
    setState(() {
      if (product.quantity < 20) {
        product.quantity++;
        _sales.add(
          SaleRecord(
            productName: product.name,
            time: DateTime.now(),
            quantity: 1,
            totalAmount: product.price,
            type: 'buy',
          ),
        );
      }
    });
    _showSnackBar('${product.name} purchased! Quantity: ${product.quantity}', Colors.green);
  }

  void _sellProduct(Product product) {
    setState(() {
      if (product.quantity > 0) {
        product.quantity--;
        _sales.add(
          SaleRecord(
            productName: product.name,
            time: DateTime.now(),
            quantity: 1,
            totalAmount: product.price,
            type: 'sell',
          ),
        );
      }
    });
    _showSnackBar('${product.name} sold! Quantity: ${product.quantity}', Colors.orange);
  }

  void _showSnackBar(String message, Color color) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: color,
        duration: Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  Color _getCategoryColor(String category) {
    switch (category) {
      case 'Electronics':
        return Colors.blue;
      case 'Food':
        return Colors.green;
      case 'Clothing':
        return Colors.purple;
      default:
        return Colors.grey;
    }
  }

  IconData _getCategoryIcon(String category) {
    switch (category) {
      case 'Electronics':
        return Icons.phone_android;
      case 'Food':
        return Icons.restaurant;
      case 'Clothing':
        return Icons.checkroom;
      default:
        return Icons.inventory_2;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFF5F5F5),
      appBar: AppBar(
        title: Text(
          'Nepal Shop Manager',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white),
        ),
        backgroundColor: Color(0xFF1E88E5),
        elevation: 8,
        actions: [
          IconButton(
            icon: Icon(Icons.dashboard, color: Colors.white),
            tooltip: "Dashboard",
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => DashboardPage(products: _products, sales: _sales),
                ),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.analytics, color: Colors.white),
            onPressed: () => _showAnalytics(),
          ),
        ],
      ),
      body: FadeTransition(
        opacity: _fadeAnimation,
        child: Column(
          children: [
            // Search and Filter Section
            Container(
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                boxShadow: [
                  BoxShadow(
                    color: Colors.grey.withOpacity(0.2),
                    spreadRadius: 2,
                    blurRadius: 8,
                    offset: Offset(0, 2),
                  ),
                ],
              ),
              child: Column(
                children: [
                  TextField(
                    controller: _searchController,
                    decoration: InputDecoration(
                      hintText: 'Search products...',
                      prefixIcon: Icon(Icons.search, color: Color(0xFF1E88E5)),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(25),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: Color(0xFFF0F0F0),
                      contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
                    ),
                    onChanged: (value) => _filterProducts(),
                  ),
                  SizedBox(height: 12),
                  Container(
                    height: 45,
                    child: ListView.builder(
                      scrollDirection: Axis.horizontal,
                      itemCount: _categories.length,
                      itemBuilder: (context, index) {
                        final category = _categories[index];
                        final isSelected = _selectedCategory == category;
                        return Padding(
                          padding: EdgeInsets.only(right: 8),
                          child: FilterChip(
                            label: Text(
                              category,
                              style: TextStyle(
                                color: isSelected ? Colors.white : Color(0xFF1E88E5),
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            selected: isSelected,
                            onSelected: (selected) {
                              setState(() {
                                _selectedCategory = category;
                                _filterProducts();
                              });
                            },
                            backgroundColor: Colors.white,
                            selectedColor: Color(0xFF1E88E5),
                            elevation: isSelected ? 4 : 2,
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
            // Products List
            Expanded(
              child: ListView.builder(
                padding: EdgeInsets.all(16),
                itemCount: _filteredProducts.length,
                itemBuilder: (context, index) {
                  final product = _filteredProducts[index];
                  return Container(
                    margin: EdgeInsets.only(bottom: 12),
                    child: Card(
                      elevation: 6,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(15),
                      ),
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(15),
                          gradient: LinearGradient(
                            colors: [Colors.white, Color(0xFFFAFAFA)],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        child: Padding(
                          padding: EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Container(
                                    padding: EdgeInsets.all(8),
                                    decoration: BoxDecoration(
                                      color: _getCategoryColor(product.category).withOpacity(0.1),
                                      borderRadius: BorderRadius.circular(8),
                                    ),
                                    child: Icon(
                                      _getCategoryIcon(product.category),
                                      color: _getCategoryColor(product.category),
                                      size: 24,
                                    ),
                                  ),
                                  SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          product.name,
                                          style: TextStyle(
                                            fontSize: 18,
                                            fontWeight: FontWeight.bold,
                                            color: Color(0xFF2C2C2C),
                                          ),
                                        ),
                                        Text(
                                          product.category,
                                          style: TextStyle(
                                            fontSize: 14,
                                            color: _getCategoryColor(product.category),
                                            fontWeight: FontWeight.w500,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                  Container(
                                    padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                                    decoration: BoxDecoration(
                                      color: product.quantity > 0 ? Colors.green.withOpacity(0.1) : Colors.red.withOpacity(0.1),
                                      borderRadius: BorderRadius.circular(20),
                                    ),
                                    child: Text(
                                      'Stock: ${product.quantity}',
                                      style: TextStyle(
                                        color: product.quantity > 0 ? Colors.green[700] : Colors.red[700],
                                        fontWeight: FontWeight.bold,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                              SizedBox(height: 12),
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'रू ${product.price.toStringAsFixed(0)}',
                                        style: TextStyle(
                                          fontSize: 20,
                                          fontWeight: FontWeight.bold,
                                          color: Color(0xFF1E88E5),
                                        ),
                                      ),
                                      Text(
                                        'per ${product.unit}',
                                        style: TextStyle(
                                          fontSize: 12,
                                          color: Colors.grey[600],
                                        ),
                                      ),
                                    ],
                                  ),
                                  Row(
                                    children: [
                                      ElevatedButton(
                                        onPressed: () => _buyProduct(product),
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Colors.green,
                                          foregroundColor: Colors.white,
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(20),
                                          ),
                                          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                          elevation: 3,
                                        ),
                                        child: Row(
                                          mainAxisSize: MainAxisSize.min,
                                          children: [
                                            Icon(Icons.add_shopping_cart, size: 16),
                                            SizedBox(width: 4),
                                            Text('Buy', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                                          ],
                                        ),
                                      ),
                                      SizedBox(width: 8),
                                      ElevatedButton(
                                        onPressed: product.quantity > 0 ? () => _sellProduct(product) : null,
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Colors.orange,
                                          foregroundColor: Colors.white,
                                          shape: RoundedRectangleBorder(
                                            borderRadius: BorderRadius.circular(20),
                                          ),
                                          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                          elevation: 3,
                                        ),
                                        child: Row(
                                          mainAxisSize: MainAxisSize.min,
                                          children: [
                                            Icon(Icons.sell, size: 16),
                                            SizedBox(width: 4),
                                            Text('Sell', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                                          ],
                                        ),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showAddProductDialog(),
        backgroundColor: Color(0xFF1E88E5),
        icon: Icon(Icons.add, color: Colors.white),
        label: Text('Add Product', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        elevation: 8,
      ),
    );
  }

  void _showAnalytics() {
    final totalProducts = _products.length;
    final totalStock = _products.fold(0, (sum, product) => sum + product.quantity);
    final totalValue = _products.fold(0.0, (sum, product) => sum + (product.quantity * product.price));
    final lowStockItems = _products.where((product) => product.quantity <= 2).length;

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Shop Analytics', style: TextStyle(fontWeight: FontWeight.bold)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildAnalyticsRow('Total Products:', totalProducts.toString()),
            _buildAnalyticsRow('Total Stock:', totalStock.toString()),
            _buildAnalyticsRow('Stock Value:', 'रू ${totalValue.toStringAsFixed(0)}'),
            _buildAnalyticsRow('Low Stock Alert:', lowStockItems.toString()),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Close'),
          ),
        ],
      ),
    );
  }

  Widget _buildAnalyticsRow(String label, String value) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label),
          Text(value, style: TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  void _showAddProductDialog() {
    final nameController = TextEditingController();
    final priceController = TextEditingController();
    final unitController = TextEditingController();
    String selectedCategory = 'Electronics';

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setState) => AlertDialog(
          title: Text('Add New Product'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: InputDecoration(labelText: 'Product Name'),
              ),
              SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: selectedCategory,
                decoration: InputDecoration(labelText: 'Category'),
                items: ['Electronics', 'Food', 'Clothing']
                    .map((cat) => DropdownMenuItem(value: cat, child: Text(cat)))
                    .toList(),
                onChanged: (value) => setState(() => selectedCategory = value!),
              ),
              SizedBox(height: 12),
              TextField(
                controller: priceController,
                decoration: InputDecoration(labelText: 'Price (रू)'),
                keyboardType: TextInputType.number,
              ),
              SizedBox(height: 12),
              TextField(
                controller: unitController,
                decoration: InputDecoration(labelText: 'Unit (kg, piece, liter)'),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                if (nameController.text.isNotEmpty &&
                    priceController.text.isNotEmpty &&
                    unitController.text.isNotEmpty) {
                  final newProduct = Product(
                    name: nameController.text,
                    category: selectedCategory,
                    price: double.parse(priceController.text),
                    unit: unitController.text,
                  );
                  setState(() {
                    _products.add(newProduct);
                    _filterProducts();
                  });
                  Navigator.pop(context);
                  _showSnackBar('Product added successfully!', Colors.green);
                }
              },
              child: Text('Add'),
            ),
          ],
        ),
      ),
    );
  }
}