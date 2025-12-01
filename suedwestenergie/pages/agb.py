"""AGB-Seite"""

import reflex as rx
from suedwestenergie.components import navbar, footer
from suedwestenergie.config import Config


def agb() -> rx.Component:
    """Allgemeine Geschäftsbedingungen"""
    return rx.fragment(
        navbar(),
        rx.box(
            rx.container(
                rx.vstack(
                    rx.heading("Allgemeine Geschäftsbedingungen", size="8", color=Config.TEXT_DARK, margin_bottom="2rem"),
                    rx.vstack(
                        rx.heading("§ 1 Geltungsbereich", size="5", color=Config.TEXT_DARK),
                        rx.text(
                            "Diese Allgemeinen Geschäftsbedingungen gelten für alle Verträge zwischen Südwest-Energie GmbH und ihren Kunden über die Vermittlung von Energieverträgen.",
                            color=Config.TEXT_DARK,
                            line_height="1.6",
                        ),
                        rx.heading("§ 2 Leistungsumfang", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text(
                            "Südwest-Energie vermittelt als unabhängiger Makler Strom- und Gasverträge zwischen Kunden und Energieversorgern. Die Vermittlung erfolgt unverbindlich und kostenfrei für den Kunden.",
                            color=Config.TEXT_DARK,
                            line_height="1.6",
                        ),
                        rx.heading("§ 3 Vertragsschluss", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text(
                            "Der Vertrag kommt direkt zwischen dem Kunden und dem Energieversorger zustande. Südwest-Energie ist nicht Vertragspartner des Energieliefervertrags.",
                            color=Config.TEXT_DARK,
                            line_height="1.6",
                        ),
                        rx.heading("§ 4 Vergütung", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text(
                            "Die Dienstleistung von Südwest-Energie ist für den Kunden vollständig kostenfrei. Die Vergütung erfolgt durch Provisionen der vermittelten Energieversorger.",
                            color=Config.TEXT_DARK,
                            line_height="1.6",
                        ),
                        align="start",
                        spacing="3",
                    ),
                    align="start",
                    padding_y="5rem",
                    max_width="800px",
                ),
                max_width="1200px",
            ),
            min_height="60vh",
        ),
        footer(),
    )