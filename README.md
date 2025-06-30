# Pasale: Hyper-Local Retail Data Platform for Nepal

Pasale is a simple, clean, and powerful Flutter application designed to digitize Nepal’s massive but largely offline retail sector. By making retail management easy and accessible for local shopkeepers, Pasale brings real-time inventory, sales tracking, and valuable analytics into the hands of 300,000+ stores across Nepal..

---

## ✨ Features

- **Nepali Language Support:** Entire app is available in Nepali for easy use.
- **Voice Command Integration:** Shopkeepers can add sales or inventory via voice, making entry effortless.
- **Easy Inventory & Sales Tracking:** Simple forms to add and manage inventory and daily sales.
- **Cloud Backup & Sync:** All data is automatically backed up and synced securely.
- **Insights & Analytics:** Shopkeepers instantly see trends, top products, and recommendations powered by AI.
- **Free Training & Incentives:** Onboarding flows and tutorials included to help users start quickly.

---

### Prerequisites

- [Flutter SDK](https://docs.flutter.dev/get-started/install) (v3.0 or higher recommended)
- [Dart SDK](https://dart.dev/get-dart) (usually shipped with Flutter)
- A device/emulator (Android/iOS)

### Flutter Dependencies

Make sure your `pubspec.yaml` includes the following essentials (add or update as needed):

```yaml
dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  provider: ^6.0.5
  cloud_firestore: ^4.13.0
  firebase_core: ^2.24.2
  google_fonts: ^6.2.1
  speech_to_text: ^6.6.0
  intl: ^0.19.0
  flutter_localizations:
    sdk: flutter
  shared_preferences: ^2.2.2
  # Add more as needed for UI, charts, etc.
```

Run the following command in your project root to install dependencies:
```sh
flutter pub get
```

### Firebase Setup (if using Firestore/Cloud backup)
1. [Set up Firebase for your Flutter app.](https://firebase.flutter.dev/docs/overview)
2. Download `google-services.json` (Android) or `GoogleService-Info.plist` (iOS) and add to platform folders as instructed.

---

## How to Run

1. **Clone the repository:**
   ```sh
   git clone https://github.com/theaayushdev/Code2Convert_HackForBusiness.git
   cd Code2Convert_HackForBusiness
   ```

2. **Install dependencies:**
   ```sh
   flutter pub get
   ```

3. **Run on an emulator or device:**
   ```sh
   flutter run
   ```

4. **For iOS:**  
   Open `ios/` in Xcode, install pods with `pod install`, and ensure a valid iOS development environment.

---

## 🔍 Usage

- **Add Inventory / Sales:** Tap the plus (+) button, fill in the form, or use the microphone for voice input.
- **View Insights:** See the dashboard for trends, top products, and suggestions.
- **Settings & Onboarding:** Access app settings, language, and tutorials from the side menu.

---

> Empowering small retailers in Nepal with simple, smart, and local digital tools.
