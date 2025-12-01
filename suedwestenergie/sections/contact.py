"""Contact Section - Kontaktformular"""

import reflex as rx
from suedwestenergie.config import Config
from suedwestenergie.state import ContactFormState
from suedwestenergie.utils.analytics import track_form_submission


def contact_section() -> rx.Component:
    """Kontakt Section mit Formular"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading("Jetzt Kontakt aufnehmen", size="8", color=Config.TEXT_DARK, text_align="center", margin_bottom="1rem"),
                rx.text("Fordern Sie unverbindlich ein individuelles Angebot an", font_size="1.2rem", color=Config.TEXT_LIGHT, text_align="center", margin_bottom="3rem"),
                rx.box(
                    rx.vstack(
                        rx.cond(
                            # Show error message if there's one
                            ContactFormState.error_message != "",
                            rx.box(
                                rx.text(ContactFormState.error_message, color="red", text_align="center"),
                                width="100%",
                                padding="10px",
                                border="1px solid red",
                                border_radius="5px",
                                background="rgba(255,0,0,0.1)",
                            ),
                        ),
                        rx.form(
                            rx.vstack(
                                rx.input(
                                    placeholder="Ihr Name *",
                                    name="name",
                                    value=ContactFormState.name,
                                    on_change=ContactFormState.set_name,
                                    required=True,
                                    padding="1rem",
                                    border=f"1px solid {Config.TEXT_LIGHT}",
                                    border_radius="8px",
                                    width="100%",
                                    min_width="250px",
                                ),
                                rx.input(
                                    placeholder="E-Mail-Adresse *",
                                    name="email",
                                    type="email",
                                    value=ContactFormState.email,
                                    on_change=ContactFormState.set_email,
                                    required=True,
                                    padding="1rem",
                                    border=f"1px solid {Config.TEXT_LIGHT}",
                                    border_radius="8px",
                                    width="100%",
                                    min_width="250px",
                                ),
                                rx.input(
                                    placeholder="Telefonnummer",
                                    name="phone",
                                    value=ContactFormState.phone,
                                    on_change=ContactFormState.set_phone,
                                    padding="1rem",
                                    border=f"1px solid {Config.TEXT_LIGHT}",
                                    border_radius="8px",
                                    width="100%",
                                    min_width="250px",
                                ),
                                rx.input(
                                    placeholder="Firmenname *",
                                    name="company",
                                    value=ContactFormState.company,
                                    on_change=ContactFormState.set_company,
                                    required=True,
                                    padding="1rem",
                                    border=f"1px solid {Config.TEXT_LIGHT}",
                                    border_radius="8px",
                                    width="100%",
                                    min_width="250px",
                                ),
                                rx.text_area(
                                    placeholder="Ihre Nachricht (mindestens 10 Zeichen)",
                                    name="message",
                                    value=ContactFormState.message,
                                    on_change=ContactFormState.set_message,
                                    padding="1rem",
                                    border=f"1px solid {Config.TEXT_LIGHT}",
                                    border_radius="8px",
                                    width="100%",
                                    min_height="120px",
                                    min_width="250px",
                                ),
                                rx.button(
                                    "🌱 Angebot anfordern",
                                    type="submit",
                                    background=Config.ACCENT_COLOR,
                                    color="white",
                                    padding="1rem 2rem",
                                    font_size="1.1rem",
                                    font_weight="600",
                                    border_radius="8px",
                                    width="100%",
                                    cursor="pointer",
                                    _hover={
                                        "background": Config.SECONDARY_COLOR,
                                        "transform": "scale(1.02)",
                                    },
                                    # Track button click
                                    on_click=lambda: track_form_submission("contact_form"),
                                ),
                                rx.text("* Pflichtfelder", font_size="0.9rem", color=Config.TEXT_LIGHT),
                                spacing="4",
                                width="100%",
                            ),
                            on_submit=ContactFormState.submit_form,
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                        align="center",
                    ),
                    background=Config.CARD_BG,
                    padding="3rem",
                    border_radius="12px",
                    border=f"2px solid {Config.BG_DARK}",
                    box_shadow="0 2px 8px rgba(45,80,22,0.1)",
                    max_width="600px",
                    width="100%",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("📧", font_size="2rem"),
                        rx.text(Config.EMAIL, color=Config.TEXT_LIGHT, font_weight="500"),
                        align="center",
                    ),
                    rx.vstack(
                        rx.text("📞", font_size="2rem"),
                        rx.text(Config.PHONE, color=Config.TEXT_LIGHT, font_weight="500"),
                        align="center",
                    ),
                    rx.vstack(
                        rx.text("📍", font_size="2rem"),
                        rx.text(Config.ADDRESS, color=Config.TEXT_LIGHT, font_weight="500"),
                        align="center",
                    ),
                    spacing="8",
                    margin_top="3rem",
                    justify="center",
                    flex_wrap="wrap",
                ),
                spacing="4",
                padding_y="5rem",
                align="center",
            ),
            max_width="1200px",
        ),
        id="kontakt",
        background=Config.BG_LIGHT,
        width="100%",
    )