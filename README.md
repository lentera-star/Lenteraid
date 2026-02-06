# LENTERA DreamFlow

![Progress](https://img.shields.io/badge/Progress-75%25-yellow)
![Sprint](https://img.shields.io/badge/Sprint-2%20Complete-success)
![Status](https://img.shields.io/badge/Status-Maintenance%20Mode-blue)
![Last Updated](https://img.shields.io/badge/Updated-Jan%202026-informational)

**LENTERA** adalah aplikasi kesehatan mental AI-powered yang menggabungkan mood tracking, konseling online dengan psikolog profesional, dan AI chatbot untuk dukungan emosional 24/7.

## 📊 Project Status (Jan 11, 2026)

- **Current Sprint**: Study Break Period (Week 5-6)
- **Completion**: 75% (Core features complete)
- **Next Milestone**: Sprint 3 Integration (starts Jan 12)
- **Total Lines of Code**: 12,000+
- **Screens**: 16 | **Models**: 6 | **Services**: 9

> 🎓 **Note**: Development in maintenance mode (Jan 1-11) untuk exam period. Full-speed development resumes Jan 12, 2026.

---

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
- Email: lenteraina2025@gmail.com
- GitHub: [@lentera-star](https://github.com/lentera-star)
