"""Services Section - Leistungsübersicht"""

import reflex as rx
from suedwestenergie.config import Config
from suedwestenergie.components import feature_card


def services_section() -> rx.Component:
    """Leistungen Section"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading("Unsere Leistungen", size="8", color=Config.TEXT_DARK, text_align="center", margin_bottom="1rem", width="100%"),
                rx.text("Professionelle Energievermittlung für Ihr Unternehmen", font_size="1.2rem", color=Config.TEXT_LIGHT, text_align="center", margin_bottom="3rem", width="100%"),
                rx.grid(
                    feature_card("⚡", "Stromvermittlung", "Wir finden den optimalen Stromtarif für Ihr Unternehmen – unabhängig, transparent und mit garantierten Einsparungen."),
                    feature_card("🔥", "Gasvermittlung", "Profitieren Sie von unseren Gasverträgen mit führenden Anbietern und senken Sie nachhaltig Ihre Heizkosten."),
                    feature_card("📊", "Marktanalyse", "Wir beobachten kontinuierlich den Energiemarkt und informieren Sie über optimale Einkaufszeitpunkte."),
                    feature_card("💼", "Vertragsmanagement", "Lückenlose Betreuung von der Angebotseinholung über Vertragsverhandlung bis zur Vertragsverlängerung."),
                    feature_card("🎯", "Trancheneinkauf", "Für Großverbraucher: Gestaffelter Energieeinkauf zur Risikominimierung und Kostenoptimierung."),
                    feature_card("🌱", "Grüne Energie", "Umstellung auf nachhaltige Energiequellen ohne Mehrkosten – gut für Umwelt und Image."),
                    columns=rx.breakpoints(initial="1", sm="1", md="2", lg="3"),
                    spacing="6",
                    width="100%",
                    justify_items="center",
                ),
                spacing="4",
                padding_y="5rem",
                align="center",
                width="100%",
            ),
            max_width="1200px",
            padding_x="1rem",  # Add some horizontal padding on small screens
            margin_x="auto",
        ),
        id="leistungen",
        background=Config.BG_LIGHT,
        width="100%",
    )