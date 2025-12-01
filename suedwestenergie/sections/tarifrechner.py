"""Tarifrechner Section - External Calculator Embed"""

import reflex as rx
from suedwestenergie.config import Config


def tarifrechner_section() -> rx.Component:
    """Tarifrechner Section - embeds external tariff calculator"""
    
    # Only render if enabled
    if not Config.TARIFRECHNER_ENABLED:
        return rx.fragment()
    
    # Prepare embed content based on type
    if Config.TARIFRECHNER_TYPE == "iframe" and Config.TARIFRECHNER_URL:
        embed_content = rx.html(
            f"""
            <iframe 
                src="{Config.TARIFRECHNER_URL}"
                width="100%"
                height="{Config.TARIFRECHNER_HEIGHT}"
                frameborder="0"
                scrolling="auto"
                style="border: 2px solid {Config.BG_DARK}; border-radius: 12px;"
            ></iframe>
            """
        )
    elif Config.TARIFRECHNER_TYPE == "script" and Config.TARIFRECHNER_SCRIPT:
        embed_content = rx.html(Config.TARIFRECHNER_SCRIPT)
    else:
        # Placeholder if no embed code configured
        embed_content = rx.box(
            rx.vstack(
                rx.text("🔧", font_size="4rem", margin_bottom="1rem"),
                rx.heading(
                    "Tarifrechner",
                    size="6",
                    color=Config.TEXT_DARK,
                    margin_bottom="0.5rem"
                ),
                rx.text(
                    "Konfigurieren Sie den Tarifrechner in der .env Datei",
                    color=Config.TEXT_LIGHT,
                    text_align="center",
                ),
                align="center",
                spacing="2",
            ),
            background=Config.BG_LIGHT,
            padding="3rem",
            border_radius="12px",
            border=f"2px dashed {Config.SECONDARY_COLOR}",
            min_height="400px",
            display="flex",
            align_items="center",
            justify_content="center",
        )
    
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Tarifrechner",
                    size="8",
                    color=Config.TEXT_DARK,
                    text_align="center",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Berechnen Sie Ihre potenzielle Ersparnis",
                    font_size="1.2rem",
                    color=Config.TEXT_LIGHT,
                    text_align="center",
                    margin_bottom="3rem",
                ),
                rx.box(
                    embed_content,
                    width="100%",
                ),
                spacing="4",
                padding_y="5rem",
            ),
            max_width="1200px",
        ),
        id="tarifrechner",
        background="white",
        width="100%",
    )
