"""Footer Komponente"""

import reflex as rx
from suedwestenergie.config import Config


def footer() -> rx.Component:
    """Footer"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading(Config.COMPANY_NAME, size="6", color="white", margin_bottom="1rem"),
                        rx.text(
                            "Ihr unabhängiger Partner für professionelle Energievermittlung",
                            color="rgba(255,255,255,0.8)",
                            max_width="300px",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.heading("Links", size="5", color="white", margin_bottom="1rem"),
                        rx.link("Startseite", href="/", color="rgba(255,255,255,0.8)"),
                        rx.link("Leistungen", href="/#leistungen", color="rgba(255,255,255,0.8)"),
                        rx.link("Vorteile", href="/#vorteile", color="rgba(255,255,255,0.8)"),
                        rx.link("Über uns", href="/#ueber-uns", color="rgba(255,255,255,0.8)"),
                        rx.link("Kontakt", href="/#kontakt", color="rgba(255,255,255,0.8)"),
                        align="start",
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.heading("Kontakt", size="5", color="white", margin_bottom="1rem"),
                        rx.text(f"📧 {Config.EMAIL}", color="rgba(255,255,255,0.8)"),
                        rx.text(f"📞 {Config.PHONE}", color="rgba(255,255,255,0.8)"),
                        rx.text(f"📍 {Config.ADDRESS}", color="rgba(255,255,255,0.8)"),
                        align="start",
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.heading("Rechtliches", size="5", color="white", margin_bottom="1rem"),
                        rx.link("Impressum", href="/impressum", color="rgba(255,255,255,0.8)"),
                        rx.link("Datenschutz", href="/datenschutz", color="rgba(255,255,255,0.8)"),
                        rx.link("AGB", href="/agb", color="rgba(255,255,255,0.8)"),
                        align="start",
                        spacing="2",
                    ),
                    spacing="8",
                    justify="between",
                    width="100%",
                    flex_wrap="wrap",
                    align="start",
                ),
                rx.divider(margin_y="2rem", border_color="rgba(255,255,255,0.2)"),
                rx.text(
                    f"© 2025 {Config.COMPANY_NAME}. Alle Rechte vorbehalten.",
                    color="rgba(255,255,255,0.6)",
                    text_align="center",
                    font_size="0.9rem",
                ),
                spacing="4",
                padding_y="3rem",
            ),
            max_width="1200px",
        ),
        background=Config.TEXT_DARK,
        width="100%",
    )