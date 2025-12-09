"""Danke-Seite nach Kontaktformular"""

import reflex as rx
from suedwestenergie.components import navbar, footer
from suedwestenergie.config import Config


def thank_you() -> rx.Component:
    """Thank You Page"""
    return rx.fragment(
        navbar(),
        rx.box(
            rx.container(
                rx.vstack(
                    # Add logo to the thank you page
                    rx.image(
                        src="/logo.jpg",
                        alt=Config.COMPANY_NAME,
                        height="80px",
                        width="auto",
                        margin_bottom="2rem",
                    ),
                    rx.text("✓", font_size="5rem", color=Config.SECONDARY_COLOR),
                    rx.heading("Vielen Dank für Ihre Anfrage!", size="8", color=Config.TEXT_DARK, text_align="center"),
                    rx.text(
                        "Wir haben Ihre Nachricht erhalten und melden uns innerhalb von 24 Stunden bei Ihnen.",
                        font_size="1.2rem",
                        color=Config.TEXT_LIGHT,
                        text_align="center",
                        max_width="600px",
                    ),
                    rx.button(
                        "Zurück zur Startseite",
                        on_click=lambda: rx.redirect("/"),
                        background=Config.PRIMARY_COLOR,
                        color="white",
                        padding="1rem 2rem",
                        font_size="1.1rem",
                        border_radius="8px",
                        cursor="pointer",
                        margin_top="2rem",
                    ),
                    spacing="6",
                    align="center",
                    padding_y="5rem",  # Reduced padding
                ),
                max_width="1200px",
            ),
            min_height="80vh",
        ),
        footer(),
    )