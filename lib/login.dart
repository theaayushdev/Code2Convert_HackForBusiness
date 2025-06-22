import 'package:flutter/material.dart';
import 'shop.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  bool isLogin = true;
  bool _obscure = true;
  final _formKey = GlobalKey<FormState>();
  final _userController = TextEditingController();
  final _passController = TextEditingController();

  void _onLogin() async {
    if (_formKey.currentState!.validate()) {
      // Simulate loading and then go to ShopHomePage
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (_) => const Center(
          child: CircularProgressIndicator(color: Color(0xFF57C4DE)),
        ),
      );
      await Future.delayed(const Duration(seconds: 1));
      if (mounted) Navigator.of(context).pop(); // remove dialog
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => NepalShopApp()),
        );
      }
    }
  }

  void _onSignIn() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text("Sign In clicked! (Create account not implemented)"),
        backgroundColor: Colors.blueAccent,
      ),
    );
  }

  void _onSocial(String name) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text("$name login clicked!"),
        backgroundColor: Colors.blue,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF57C4DE),
      body: Center(
        child: SingleChildScrollView(
          child: Stack(
            children: [
              // Blue curved header
              Container(
                height: 340,
                decoration: const BoxDecoration(
                  color: Color(0xFF57C4DE),
                  borderRadius: BorderRadius.only(
                    bottomRight: Radius.circular(90),
                  ),
                ),
              ),
              Column(
                children: [
                  const SizedBox(height: 56),
                  // Header text
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 36),
                    child: Align(
                      alignment: Alignment.centerLeft,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text(
                            "Hello!",
                            style: TextStyle(
                              fontSize: 34,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(height: 6),
                          Text(
                            "Welcome to पसले",
                            style: TextStyle(
                              fontSize: 26,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 52),
                  // White card with tabs and form
                  Container(
                    margin: const EdgeInsets.symmetric(horizontal: 22),
                    padding: const EdgeInsets.symmetric(vertical: 36, horizontal: 18),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(36),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.07),
                          blurRadius: 16,
                          offset: const Offset(0, 8),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        // Tabs
                        Container(
                          decoration: BoxDecoration(
                            color: const Color(0xFFEAF8FB),
                            borderRadius: BorderRadius.circular(30),
                          ),
                          child: Row(
                            children: [
                              Expanded(
                                child: GestureDetector(
                                  onTap: () => setState(() => isLogin = true),
                                  child: Container(
                                    decoration: BoxDecoration(
                                      color: isLogin ? const Color(0xFF57C4DE) : Colors.transparent,
                                      borderRadius: BorderRadius.circular(30),
                                    ),
                                    padding: const EdgeInsets.symmetric(vertical: 14),
                                    child: Center(
                                      child: Text(
                                        "Log In",
                                        style: TextStyle(
                                          color: isLogin ? Colors.white : const Color(0xFF57C4DE),
                                          fontWeight: FontWeight.bold,
                                          fontSize: 17,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              Expanded(
                                child: GestureDetector(
                                  onTap: () => setState(() => isLogin = false),
                                  child: Container(
                                    decoration: BoxDecoration(
                                      color: !isLogin ? const Color(0xFF57C4DE) : Colors.transparent,
                                      borderRadius: BorderRadius.circular(30),
                                    ),
                                    padding: const EdgeInsets.symmetric(vertical: 14),
                                    child: Center(
                                      child: Text(
                                        "Sign In",
                                        style: TextStyle(
                                          color: !isLogin ? Colors.white : const Color(0xFF57C4DE),
                                          fontWeight: FontWeight.bold,
                                          fontSize: 17,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 22),
                        // Form
                        Form(
                          key: _formKey,
                          child: Column(
                            children: [
                              // Username
                              TextFormField(
                                controller: _userController,
                                decoration: InputDecoration(
                                  hintText: "Username or Email",
                                  contentPadding: const EdgeInsets.symmetric(vertical: 18, horizontal: 22),
                                  border: OutlineInputBorder(
                                    borderRadius: BorderRadius.circular(28),
                                    borderSide: BorderSide.none,
                                  ),
                                  filled: true,
                                  fillColor: const Color(0xFFF5FBFC),
                                ),
                                validator: (v) => v == null || v.isEmpty ? "Required" : null,
                              ),
                              const SizedBox(height: 16),
                              // Password
                              TextFormField(
                                controller: _passController,
                                obscureText: _obscure,
                                decoration: InputDecoration(
                                  hintText: "Password",
                                  contentPadding: const EdgeInsets.symmetric(vertical: 18, horizontal: 22),
                                  border: OutlineInputBorder(
                                    borderRadius: BorderRadius.circular(28),
                                    borderSide: BorderSide.none,
                                  ),
                                  filled: true,
                                  fillColor: const Color(0xFFF5FBFC),
                                  suffixIcon: IconButton(
                                    icon: Icon(_obscure ? Icons.visibility : Icons.visibility_off, color: const Color(0xFF57C4DE)),
                                    onPressed: () => setState(() => _obscure = !_obscure),
                                  ),
                                ),
                                validator: (v) => v == null || v.isEmpty ? "Required" : null,
                              ),
                              const SizedBox(height: 20),
                              SizedBox(
                                width: double.infinity,
                                height: 50,
                                child: ElevatedButton(
                                  onPressed: isLogin ? _onLogin : _onSignIn,
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: const Color(0xFF57C4DE),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                                  ),
                                  child: Text(
                                    isLogin ? "Log In" : "Sign In",
                                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 18),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Container(height: 1, width: 32, color: Colors.grey[300]),
                            const Padding(
                              padding: EdgeInsets.symmetric(horizontal: 8),
                              child: Text("or", style: TextStyle(fontSize: 14, color: Colors.black54)),
                            ),
                            Container(height: 1, width: 32, color: Colors.grey[300]),
                          ],
                        ),
                        const SizedBox(height: 10),
                        // Social buttons
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.facebook, color: Colors.blue, size: 32),
                              onPressed: () => _onSocial("Facebook"),
                            ),
                            const SizedBox(width: 8),
                            IconButton(
                              icon: const Icon(Icons.alternate_email, color: Colors.lightBlue, size: 30),
                              onPressed: () => _onSocial("Twitter"),
                            ),
                            const SizedBox(width: 8),
                            IconButton(
                              icon: const Icon(Icons.g_mobiledata, color: Colors.redAccent, size: 32),
                              onPressed: () => _onSocial("Google"),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}