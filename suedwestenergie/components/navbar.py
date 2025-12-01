"""Navigation Bar Komponente"""

import reflex as rx
from suedwestenergie.config import Config


def navbar() -> rx.Component:
    """Navigation Bar"""
    return rx.box(
        rx.container(
            rx.hstack(
                rx.heading(
                    Config.COMPANY_NAME,
                    size="7",
                    color=Config.PRIMARY_COLOR,
                    font_weight="700",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.link("Startseite", href="/", color=Config.TEXT_DARK, font_weight="500"),
                    rx.link("Leistungen", href="/#leistungen", color=Config.TEXT_DARK, font_weight="500"),
                    rx.link("Vorteile", href="/#vorteile", color=Config.TEXT_DARK, font_weight="500"),
                    rx.link("Über uns", href="/#ueber-uns", color=Config.TEXT_DARK, font_weight="500"),
                    rx.button(
                        "Kontakt",
                        on_click=lambda: rx.redirect("/#kontakt"),
                        background=Config.PRIMARY_COLOR,
                        color="white",
                        padding="0.75rem 1.5rem",
                        border_radius="8px",
                        cursor="pointer",
                        _hover={"background": Config.SECONDARY_COLOR},
                    ),
                    spacing="6",
                    display=["none", "none", "flex"],
                ),
                align="center",
                justify="between",
                width="100%",
            ),
            max_width="1200px",
            padding="1rem",
        ),
        background="white",
        box_shadow="0 2px 8px rgba(0,0,0,0.1)",
        position="sticky",
        top="0",
        z_index="100",
        width="100%",
    )