# LENTERA DreamFlow

LENTERA DreamFlow adalah aplikasi kesehatan mental yang menggabungkan mood tracking, konseling online dengan psikolog profesional, dan AI chatbot untuk dukungan emosional 24/7.

## Fitur Utama

- 🎭 **Mood Tracking**: Catat dan analisis pola mood harian Anda
- 👨‍⚕️ **Konseling Online**: Booking sesi dengan psikolog profesional
- 🤖 **AI Chatbot**: Sahabat Lentera untuk dukungan emosional 24/7
- 📊 **Insights**: Analisis mendalam tentang kesehatan mental Anda
- 🎮 **Gamifikasi**: Sistem reward dan avatar customization
- 💳 **Payment Integration**: Pembayaran mudah dan aman

## Tech Stack

### Frontend (Mobile)
- Flutter & Dart
- Provider for state management
- Supabase for authentication & database

### Backend (AI)
- Python FastAPI
- Ollama for local LLM
- Docker support

## Getting Started

### Prerequisites
- Flutter SDK (3.0+)
- Python 3.9+
- Docker (optional, for backend)
- Supabase account

### Installation

1. Clone repository:
```bash
git clone https://github.com/lentera-star/Lenteraid.git
cd Lenteraid
```

2. Install Flutter dependencies:
```bash
flutter pub get
```

3. Setup backend:
```bash
# Using PowerShell (Windows)
.\setup-backend.ps1

# Using Bash (Linux/Mac)
./setup-backend.sh
```

4. Configure Supabase:
   - Copy `.env.example` to `.env`
   - Update with your Supabase credentials

5. Run the app:
```bash
flutter run
```

## Project Structure

```
├── lib/                 # Flutter source code
│   ├── auth/           # Authentication logic
│   ├── components/     # Reusable UI components
│   ├── models/         # Data models
│   ├── screens/        # App screens
│   ├── services/       # Business logic & API calls
│   └── supabase/       # Database schema & migrations
├── backend/            # Python FastAPI backend
├── assets/             # Images, icons, fonts
└── docs/               # Documentation files
```

## Documentation

- [Architecture](architecture.md) - System architecture overview
- [Team Plan](TEAM_PLAN.md) - Development roadmap
- [Progress Report](PROGRESS_REPORT.md) - Current development status

## Contributing

We welcome contributions! Please read our contributing guidelines before submitting PRs.

## License

This project is proprietary software. All rights reserved.

## Contact

LENTERA Team
- Email: contact@lentera.id
- GitHub: [@lentera-star](https://github.com/lentera-star)
