"""Hauptseite"""

import reflex as rx
from suedwestenergie.components import navbar, footer
from suedwestenergie.sections import (
    hero_section,
    service_models_section,
    services_section,
    benefits_section,
    about_section,
    tarifrechner_section,
    contact_section,
)


def index() -> rx.Component:
    """Hauptseite"""
    return rx.fragment(
        navbar(),
        hero_section(),
        service_models_section(),
        benefits_section(),
        about_section(),
        services_section(),
        tarifrechner_section(),
        contact_section(),
        footer(),
    )