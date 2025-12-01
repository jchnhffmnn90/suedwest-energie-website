"""Benefits Section - Vorteile"""

import reflex as rx
from suedwestenergie.config import Config


def benefits_section() -> rx.Component:
    """Vorteile Section mit nachhaltiger Ausrichtung"""
    benefits = [
        (
            "🌱",
            "100% Kostenfrei",
            "Analyse und Vergleich bei über 250 Energieanbietern – vollständig kostenfrei für Sie. Unsere Vergütung erfolgt durch die Energieversorger."
        ),
        (
            "🍃",
            "Versorger-unabhängig",
            "Wir prüfen unabhängig und neutral alle Tarife. Kein Anbieter wird bevorzugt – wir erhalten für jeden die gleiche Provision."
        ),
        (
            "♻️",
            "Maximale Zeitersparnis",
            "Konzentrieren Sie sich auf Ihr Geschäft. Wir übernehmen die komplette Abwicklung – von A bis Z, inklusive aller Formalitäten."
        ),
        (
            "🌍",
            "Persönlicher Ansprechpartner",
            "Kein Callcenter, keine Hotline. Sie erhalten einen festen Ansprechpartner, der Ihre Bedürfnisse kennt und langfristig für Sie da ist."
        ),
        (
            "💚",
            "Grüne Energie",
            "Wir helfen Ihnen beim Umstieg auf nachhaltige Energiequellen – gut für die Umwelt und Ihr Image."
        ),
        (
            "🌿",
            "Automatische Optimierung",
            "Jährliche automatische Überprüfung und Optimierung Ihrer Energie-Tarife – ohne dass Sie sich darum kümmern müssen."
        ),
    ]
    
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Warum Südwest-Energie?",
                    size="8",
                    color=Config.TEXT_DARK,
                    text_align="center",
                    margin_bottom="1rem"
                ),
                rx.text(
                    "Ihre Vorteile für eine nachhaltige Zukunft",
                    font_size="1.2rem",
                    color=Config.TEXT_LIGHT,
                    text_align="center",
                    margin_bottom="3rem"
                ),
                rx.grid(
                    *[
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    icon,
                                    font_size="3rem",
                                    margin_bottom="1rem",
                                ),
                                rx.heading(
                                    title,
                                    size="5",
                                    color=Config.SECONDARY_COLOR,
                                    margin_bottom="0.5rem",
                                    text_align="center",
                                ),
                                rx.text(
                                    desc,
                                    color=Config.TEXT_LIGHT,
                                    line_height="1.6",
                                    text_align="center",
                                ),
                                align="center",
                                spacing="2",
                            ),
                            background=Config.CARD_BG,
                            padding="2rem",
                            border_radius="12px",
                            border=f"2px solid {Config.BG_DARK}",
                            box_shadow="0 2px 8px rgba(45,80,22,0.1)",
                            _hover={
                                "border_color": Config.SECONDARY_COLOR,
                                "transform": "translateY(-4px)",
                                "box_shadow": "0 6px 20px rgba(124,179,66,0.2)",
                                "transition": "all 0.3s ease",
                            },
                        )
                        for icon, title, desc in benefits
                    ],
                    columns=rx.breakpoints(initial="1", sm="1", md="2", lg="3"),
                    spacing="4",
                    width="100%",
                ),
                spacing="4",
                padding_y="5rem",
            ),
            max_width="1200px",
        ),
        background=Config.BG_LIGHT,
        width="100%",
    )