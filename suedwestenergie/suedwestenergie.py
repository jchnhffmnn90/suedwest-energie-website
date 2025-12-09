"""Haupt-App Datei"""

import reflex as rx
from suedwestenergie.pages import index, thank_you, impressum, datenschutz, agb, status_page, StatusState
from suedwestenergie.config import Config


# App erstellen
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="green",
    ),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
    style={
        "font_family": "Inter, sans-serif",
    },
    # Add Google Analytics if configured
    head_components=[
        rx.script(
            src=f"https://www.googletagmanager.com/gtag/js?id={Config.GOOGLE_ANALYTICS_ID}",
            defer=True
        ) if Config.GOOGLE_ANALYTICS_ID else rx.fragment(),
        rx.script(
            f"""
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{Config.GOOGLE_ANALYTICS_ID}', {{
                'anonymize_ip': true,
                'send_page_view': false
            }});
            """,
        ) if Config.GOOGLE_ANALYTICS_ID else rx.fragment(),
    ] if Config.GOOGLE_ANALYTICS_ID else [],
)

# Routen hinzufügen
app.add_page(index, route="/",
             title=Config.SITE_TITLE, description=Config.SITE_DESCRIPTION)
app.add_page(thank_you, route="/danke",
             title="Vielen Dank - Südwest-Energie",
             image="/logo.jpg")
app.add_page(impressum, route="/impressum",
             title=f"Impressum - {Config.COMPANY_NAME}",
             image="/logo.jpg")
app.add_page(datenschutz, route="/datenschutz",
             title=f"Datenschutz - {Config.COMPANY_NAME}",
             image="/logo.jpg")
app.add_page(agb, route="/agb",
             title=f"AGB - {Config.COMPANY_NAME}",
             image="/logo.jpg")
app.add_page(status_page, route="/status",
             title=f"System Status - {Config.COMPANY_NAME}",
             on_load=StatusState.check_services,
             image="/logo.jpg")