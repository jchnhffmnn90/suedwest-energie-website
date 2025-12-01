"""Analytics utilities for tracking and monitoring"""

import reflex as rx
from typing import Dict, Any, Optional
from suedwestenergie.config import Config


def google_analytics_script() -> Optional[rx.Component]:
    """Add Google Analytics tracking script if ID is configured"""
    if Config.GOOGLE_ANALYTICS_ID:
        return rx.script(
            f"""
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{Config.GOOGLE_ANALYTICS_ID}');
            """,
            id="gtag-script"
        )
    return None


def add_analytics_component() -> rx.Component:
    """Component to add analytics tracking to pages"""
    return rx.cond(
        Config.GOOGLE_ANALYTICS_ID != "",
        rx.script(
            f"""
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{Config.GOOGLE_ANALYTICS_ID}');
            """,
            id="gtag-script"
        ),
        rx.fragment()  # Return empty fragment if no analytics ID
    )


def track_event(event_name: str, event_params: Optional[Dict[str, Any]] = None) -> rx.event:
    """Track a custom event in Google Analytics"""
    if event_params is None:
        event_params = {}

    return rx.call_script(
        f"if(typeof gtag !== 'undefined') gtag('event', '{event_name}', {str(event_params)})"
    )


def track_page_view(title: str = "", path: str = "") -> rx.event:
    """Track a page view in Google Analytics"""
    # This will be called automatically by Google Analytics,
    # but can be called manually if needed
    tracking_params = {}
    if title:
        tracking_params["title"] = title
    if path:
        tracking_params["page_path"] = path

    return rx.call_script(
        f"if(typeof gtag !== 'undefined') gtag('event', 'page_view', {str(tracking_params)})"
    )


def track_form_submission(form_name: str) -> rx.event:
    """Track form submission events"""
    return track_event(
        "form_submit",
        {"form_name": form_name}
    )


def track_button_click(button_name: str) -> rx.event:
    """Track button click events"""
    return track_event(
        "button_click",
        {"button_name": button_name}
    )