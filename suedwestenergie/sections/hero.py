"""Hero Section - Hauptbereich der Startseite"""

import reflex as rx
from suedwestenergie.config import Config


def hero_section() -> rx.Component:
    """Hero Section mit Call-to-Action"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Nachhaltige Energielösungen für Ihr Unternehmen",
                    size="9",
                    color=Config.TEXT_DARK,
                    text_align="center",
                    font_weight="700",
                    line_height="1.2",
                ),
                rx.heading(
                    "intelligent, umweltfreundlich, kostengünstig",
                    size="7",
                    color=Config.SECONDARY_COLOR,
                    text_align="center",
                    font_weight="600",
                    margin_top="1rem",
                ),
                rx.text(
                    "Finden Sie die besten grünen Strom- und Gas-Tarife auf dem Markt. Wir vergleichen über 250 Energieversorger für Sie und unterstützen Ihren Weg zu nachhaltiger Energie – transparent, unabhängig und 100% kostenfrei.",
                    font_size="1.25rem",
                    color=Config.TEXT_LIGHT,
                    text_align="center",
                    max_width="800px",
                    margin_top="1.5rem",
                    line_height="1.6",
                ),
                rx.hstack(
                    rx.button(
                        "🌱 Jetzt kostenfrei beraten lassen",
                        on_click=lambda: rx.redirect("/#kontakt"),
                        background=Config.ACCENT_COLOR,
                        color="white",
                        padding="1rem 2rem",
                        font_size="1.1rem",
                        font_weight="600",
                        border_radius="8px",
                        cursor="pointer",
                        _hover={
                            "background": Config.SECONDARY_COLOR,
                            "transform": "scale(1.05)",
                        },
                        box_shadow="0 4px 20px rgba(124,179,66,0.3)",
                    ),
                    rx.button(
                        "Mehr erfahren",
                        on_click=lambda: rx.redirect("/#leistungen"),
                        background="transparent",
                        color=Config.PRIMARY_COLOR,
                        border=f"2px solid {Config.SECONDARY_COLOR}",
                        padding="1rem 2rem",
                        font_size="1.1rem",
                        border_radius="8px",
                        cursor="pointer",
                        _hover={
                            "background": Config.BG_LIGHT,
                            "border_color": Config.ACCENT_COLOR,
                        },
                    ),
                    spacing="4",
                    margin_top="2rem",
                    flex_wrap="wrap",
                    justify="center",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.heading("250+", size="6", color=Config.SECONDARY_COLOR),
                        rx.text("Energieversorger im Vergleich", font_size="0.9rem", color=Config.TEXT_LIGHT, text_align="center"),
                        align="center",
                    ),
                    rx.vstack(
                        rx.heading("25%", size="6", color=Config.SECONDARY_COLOR),
                        rx.text("Ø Kostenersparnis", font_size="0.9rem", color=Config.TEXT_LIGHT),
                        align="center",
                    ),
                    rx.vstack(
                        rx.heading("100%", size="6", color=Config.SECONDARY_COLOR),
                        rx.text("Grüne Optionen", font_size="0.9rem", color=Config.TEXT_LIGHT),
                        align="center",
                    ),
                    spacing="8",
                    margin_top="3rem",
                    justify="center",
                    flex_wrap="wrap",
                ),
                spacing="4",
                align="center",
                padding_y="5rem",
            ),
            max_width="1200px",
        ),
        background=f"linear-gradient(135deg, {Config.BG_LIGHT} 0%, {Config.BG_DARK} 100%)",
        width="100%",
    )