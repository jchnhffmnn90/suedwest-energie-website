"""About Section - Über uns"""

import reflex as rx
from suedwestenergie.config import Config


def about_section() -> rx.Component:
    """Über uns Section"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading("Über Südwest-Energie", size="8", color=Config.TEXT_DARK, text_align="center", margin_bottom="1rem"),
                rx.text("Ihr Partner für intelligente und nachhaltige Energielösungen", font_size="1.2rem", color=Config.TEXT_LIGHT, text_align="center", margin_bottom="3rem"),
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Südwest-Energie ist Ihr unabhängiger Partner für professionelle Energievermittlung im Südwesten Deutschlands. Mit über 10 Jahren Erfahrung am Energiemarkt haben wir bereits über 500 Unternehmen zu nachhaltig günstigeren Energiekosten verholfen.",
                            font_size="1.1rem",
                            color=Config.TEXT_LIGHT,
                            line_height="1.8",
                            margin_bottom="1rem",
                        ),
                        rx.text(
                            "Unser Team aus Energieexperten kennt den Markt und verfügt über exzellente Kontakte zu allen relevanten Versorgern. Diese Expertise kombinieren wir mit modernster Technologie, um für jedes Unternehmen – egal ob Kleinbetrieb oder Industrieunternehmen – die optimale Energielösung zu finden.",
                            font_size="1.1rem",
                            color=Config.TEXT_LIGHT,
                            line_height="1.8",
                            margin_bottom="1rem",
                        ),
                        rx.text(
                            "🌱 Nachhaltigkeit und Umweltschutz liegen uns am Herzen. Wir unterstützen Unternehmen aktiv beim Umstieg auf grüne Energie und erneuerbare Energiequellen. Gemeinsam gestalten wir eine umweltfreundliche Zukunft – wirtschaftlich sinnvoll und ökologisch verantwortungsvoll.",
                            font_size="1.1rem",
                            color=Config.TEXT_DARK,
                            font_weight="500",
                            line_height="1.8",
                            margin_bottom="1rem",
                            padding="1rem",
                            background=Config.BG_LIGHT,
                            border_radius="8px",
                            border_left=f"4px solid {Config.SECONDARY_COLOR}",
                        ),
                        rx.text(
                            "Wir sind stolz auf unsere langjährigen Kundenbeziehungen. Für uns steht nicht die schnelle Provision im Vordergrund, sondern Ihre langfristige Zufriedenheit und messbare Kostenersparnis. Lassen Sie uns gemeinsam Ihre Energiekosten senken!",
                            font_size="1.1rem",
                            color=Config.TEXT_LIGHT,
                            line_height="1.8",
                        ),
                        align="start",
                        spacing="3",
                    ),
                    background=Config.CARD_BG,
                    padding="3rem",
                    border_radius="12px",
                    border=f"2px solid {Config.BG_DARK}",
                    box_shadow="0 2px 8px rgba(45,80,22,0.1)",
                    max_width="900px",
                ),
                spacing="4",
                padding_y="5rem",
                align="center",
            ),
            max_width="1200px",
        ),
        id="ueber-uns",
        background="white",
        width="100%",
    )