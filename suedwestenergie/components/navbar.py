"""Navigation Bar Komponente"""

import reflex as rx
from suedwestenergie.config import Config


def navbar() -> rx.Component:
    """Navigation Bar"""
    return rx.box(
        rx.container(
            # For mobile: Stack items vertically and center
            rx.vstack(
                # Logo and company name row
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        alt=Config.COMPANY_NAME,
                        height="40px",
                        width="auto",
                        margin_right="1rem",
                    ),
                    rx.heading(
                        Config.COMPANY_NAME,
                        size="7",
                        color="#2E7D32",  # Darker green
                        font_weight="700",
                    ),
                    align="center",
                    justify="center",
                    width="100%",
                    padding_y="0.5rem",
                ),
                # Navigation links row
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
                    justify="center",
                    align="center",
                    width="100%",
                    padding_y="0.5rem",
                ),
                spacing="4",
                align="center",
                width="100%",
                # Show as row on larger screens
                display=["flex", "flex", "flex"],
                flex_direction=["column", "column", "row"],
            ),
            max_width="1200px",
            padding="1rem",
            margin_x="auto",
        ),
        background="white",
        box_shadow="0 2px 8px rgba(0,0,0,0.1)",
        position="sticky",
        top="0",
        z_index="100",
        width="100%",
    )