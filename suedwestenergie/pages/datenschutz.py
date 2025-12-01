"""Datenschutz-Seite"""

import reflex as rx
from suedwestenergie.components import navbar, footer
from suedwestenergie.config import Config


def datenschutz() -> rx.Component:
    """Datenschutzerklärung"""
    return rx.fragment(
        navbar(),
        rx.box(
            rx.container(
                rx.vstack(
                    rx.heading("Datenschutzerklärung", size="8", color=Config.TEXT_DARK, margin_bottom="2rem"),
                    rx.vstack(
                        rx.heading("1. Datenschutz auf einen Blick", size="5", color=Config.TEXT_DARK),
                        rx.text(
                            "Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie unsere Website besuchen.",
                            color=Config.TEXT_DARK,
                            line_height="1.6",
                        ),
                        rx.heading("2. Allgemeine Hinweise und Pflichtinformationen", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text(
                            "Die Betreiber dieser Seiten nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Wir behandeln Ihre personenbezogenen Daten vertraulich und entsprechend der gesetzlichen Datenschutzvorschriften sowie dieser Datenschutzerklärung.",
                            color=Config.TEXT_DARK,
                            line_height="1.6",
                        ),
                        rx.heading("3. Datenerfassung auf unserer Website", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text(
                            "Wenn Sie uns per Kontaktformular Anfragen zukommen lassen, werden Ihre Angaben aus dem Anfrageformular inklusive der von Ihnen dort angegebenen Kontaktdaten zwecks Bearbeitung der Anfrage und für den Fall von Anschlussfragen bei uns gespeichert.",
                            color=Config.TEXT_DARK,
                            line_height="1.6",
                        ),
                        rx.heading("4. Ihre Rechte", size="5", color=Config.TEXT_DARK, margin_top="2rem"),
                        rx.text(
                            "Sie haben jederzeit das Recht auf unentgeltliche Auskunft über Ihre gespeicherten personenbezogenen Daten, deren Herkunft und Empfänger und den Zweck der Datenverarbeitung sowie ein Recht auf Berichtigung oder Löschung dieser Daten.",
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