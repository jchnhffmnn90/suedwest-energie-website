"""Impressum-Seite"""

import reflex as rx
from suedwestenergie.components import navbar, footer
from suedwestenergie.config import Config


def impressum() -> rx.Component:
    """Impressum"""
    return rx.fragment(
        navbar(),
        rx.box(
            rx.container(
                rx.vstack(
                    rx.heading("Impressum", size="8", color=Config.TEXT_DARK, margin_bottom="2rem"),
                    rx.vstack(
                        rx.heading("Angaben gemäß § 5 TMG", size="5", color=Config.TEXT_DARK),
                        rx.text("Südwest-Energie GmbH", color=Config.TEXT_DARK),
                        rx.text("Musterstraße 123", color=Config.TEXT_DARK),
                        rx.text("70173 Stuttgart", color=Config.TEXT_DARK),
                        rx.heading("Vertreten durch:", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text("Max Mustermann (Geschäftsführer)", color=Config.TEXT_DARK),
                        rx.heading("Kontakt:", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text(f"Telefon: {Config.PHONE}", color=Config.TEXT_DARK),
                        rx.text(f"E-Mail: {Config.EMAIL}", color=Config.TEXT_DARK),
                        rx.heading("Registereintrag:", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text("Eintragung im Handelsregister", color=Config.TEXT_DARK),
                        rx.text("Registergericht: Amtsgericht Stuttgart", color=Config.TEXT_DARK),
                        rx.text("Registernummer: HRB 123456", color=Config.TEXT_DARK),
                        rx.heading("Umsatzsteuer-ID:", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text("DE123456789", color=Config.TEXT_DARK),
                        align="start",
                        spacing="2",
                    ),
                    align="start",
                    padding_y="5rem",
                    max_width="800px",
                ),
                max_width="1200px",
            ),
            min_height="60vh",
        ),
        footer(),
    )