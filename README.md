# Südwest-Energie Website

Professionelle Energievermittlung für Unternehmen - Built with Reflex

## 🚀 Installation

```bash
# Virtual Environment erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# Reflex initialisieren
reflex init
```

## 💻 Development

```bash
# Development Server starten
reflex run

# Production Build
reflex export
```

## 📁 Projektstruktur

```
suedwestenergie/
├── .gitignore
├── requirements.txt
├── rxconfig.py
├── README.md
└── suedwestenergie/
    ├── __init__.py
    ├── suedwestenergie.py (Haupt-App)
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    ├── state/
    │   ├── __init__.py
    │   └── contact_state.py
    ├── components/
    │   ├── __init__.py
    │   ├── navbar.py
    │   ├── footer.py
    │   └── cards.py
    ├── pages/
    │   ├── __init__.py
    │   ├── index.py
    │   ├── thank_you.py
    │   ├── impressum.py
    │   ├── datenschutz.py
    │   └── agb.py
    └── sections/
        ├── __init__.py
        ├── hero.py
        ├── services.py
        ├── benefits.py
        ├── target_groups.py
        ├── about.py
        └── contact.py
```

## ⚙️ Anpassungen

- **Farben & Branding**: `config/settings.py`
- **Kontaktdaten**: `config/settings.py`
- **Inhalte**: Jeweilige Komponenten in `sections/` und `pages/`

## 📞 Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue.

## 🏗️ Production Deployment

For production deployment, this application has been enhanced with the following features:

- **Security enhancements**: Form validation, input sanitization, security headers
- **Error handling & logging**: Comprehensive error tracking and logging system
- **Performance optimization**: Caching mechanisms and compression
- **Analytics**: Google Analytics integration for monitoring
- **Environment configuration**: Secure environment variable management
- **Production deployment**: Docker and docker-compose setup for production

See the [PRODUCTION.md](PRODUCTION.md) file for detailed production deployment instructions.

