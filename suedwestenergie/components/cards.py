"""Wiederverwendbare Card-Komponenten"""

import reflex as rx
from suedwestenergie.config import Config


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    """Feature Card Component"""
    return rx.box(
        rx.vstack(
            rx.text(icon, font_size="3rem", margin_bottom="1rem"),
            rx.heading(title, size="5", color=Config.SECONDARY_COLOR, margin_bottom="0.5rem"),
            rx.text(description, color=Config.TEXT_LIGHT, text_align="center", line_height="1.6"),
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
            "transform": "translateY(-5px)",
            "box_shadow": "0 6px 20px rgba(124,179,66,0.2)",
        },
        transition="all 0.3s ease",
        width="100%",
        min_height="280px",
    )