"""Service Models Section - Energiebeschaffungsmodelle"""

import reflex as rx
from suedwestenergie.config import Config


def service_models_section() -> rx.Component:
    """Service Models Section - zeigt verschiedene Energiebeschaffungsmodelle"""
    
    models = [
        {
            "title": "Terminmarkt",
            "subtitle": "Festpreismodell",
            "description": "Planungssicherheit durch Festpreise – langfristige Absicherung gegen Preisschwankungen für Ihr Unternehmen.",
            "icon": "🌱",
        },
        {
            "title": "Spotmarkt",
            "subtitle": "Tagesmarkt",
            "description": "Profitieren Sie von den tagesaktuellen Marktpreisen und flexibler Energiebeschaffung am Spotmarkt.",
            "icon": "⚡",
        },
        {
            "title": "Trancheneinkauf",
            "subtitle": "Gestaffelter Einkauf",
            "description": "Gestaffelter Energieeinkauf für maximale Flexibilität und marktnahe Konditionen – optimal für volatile Märkte.",
            "icon": "🌿",
        },
    ]
    
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Ihre Energiebeschaffung mit Südwest-Energie",
                    size="8",
                    color=Config.TEXT_DARK,
                    text_align="center",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Wir bieten Ihnen flexible Beschaffungsmodelle für optimale Energiekosten",
                    font_size="1.2rem",
                    color=Config.TEXT_LIGHT,
                    text_align="center",
                    margin_bottom="3rem",
                ),
                rx.grid(
                    *[
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    model["icon"],
                                    font_size="3rem",
                                    margin_bottom="1rem",
                                ),
                                rx.heading(
                                    model["title"],
                                    size="6",
                                    color=Config.SECONDARY_COLOR,
                                    margin_bottom="0.5rem",
                                ),
                                rx.text(
                                    model["subtitle"],
                                    font_size="1rem",
                                    color=Config.TEXT_LIGHT,
                                    font_style="italic",
                                    margin_bottom="1rem",
                                ),
                                rx.text(
                                    model["description"],
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
                        for model in models
                    ],
                    columns=rx.breakpoints(initial="1", sm="1", md="3"),
                    spacing="4",
                    width="100%",
                ),
                spacing="4",
                padding_y="5rem",
            ),
            max_width="1200px",
        ),
        background="white",
        width="100%",
    )

