"""Sections package - contains all page sections"""

from .hero import hero_section
from .about import about_section
from .services import services_section
from .benefits import benefits_section
from .contact import contact_section
from .service_models import service_models_section
from .tarifrechner import tarifrechner_section

__all__ = [
    "hero_section",
    "about_section",
    "services_section",
    "benefits_section",
    "contact_section",
    "service_models_section",
    "tarifrechner_section",
]