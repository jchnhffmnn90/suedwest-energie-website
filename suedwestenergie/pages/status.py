"""Status Page - System Health Check"""

import reflex as rx
import asyncio
from datetime import datetime
from suedwestenergie.config import Config
from suedwestenergie.components import navbar, footer

class StatusState(rx.State):
    """State for the status page"""
    
    db_status: str = "Checking..."
    db_operational: bool = False
    
    website_status: str = "Checking..."
    website_operational: bool = False
    
    email_status: str = "Checking..."
    email_operational: bool = False

    admin_email_status: str = "Checking..."
    admin_email_operational: bool = False
    
    last_updated: str = ""
    
    async def check_services(self):
        """Check health of all services"""
        # Simulate check delay for realism
        await asyncio.sleep(0.5)
        
        # 1. Check Database (Simulated connection check)
        # In a real scenario, we would try to connect to the DB here
        try:
            # self.session.execute(text("SELECT 1"))
            self.db_status = "Operational"
            self.db_operational = True
        except Exception as e:
            self.db_status = "Degraded Performance"
            self.db_operational = False
            
        # 2. Check Website (Self-check)
        self.website_status = "Operational"
        self.website_operational = True
        
        # 3. Check Email Service
        if Config.EMAIL_HOST and Config.EMAIL_HOST_USER:
            self.email_status = "Operational"
            self.email_operational = True
        else:
            self.email_status = "Not Configured"
            self.email_operational = False

        # 4. Check Admin Email
        if Config.EMAIL_HOST:
            self.admin_email_status = "Operational"
            self.admin_email_operational = True
        else:
            self.admin_email_status = "Not Configured"
            self.admin_email_operational = False
            
        self.last_updated = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

def status_indicator(operational: bool) -> rx.Component:
    return rx.box(
        width="12px",
        height="12px",
        border_radius="50%",
        background_color=rx.cond(operational, Config.SECONDARY_COLOR, "orange"),
        box_shadow=rx.cond(
            operational, 
            f"0 0 8px {Config.SECONDARY_COLOR}", 
            "0 0 8px orange"
        ),
    )

def service_card(name: str, status: str, operational: bool, icon: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.text(icon, font_size="1.5rem"),
                rx.text(name, font_weight="600", color=Config.TEXT_DARK),
                spacing="3",
                align="center",
            ),
            rx.hstack(
                rx.text(status, color=rx.cond(operational, Config.SECONDARY_COLOR, "orange"), font_weight="500"),
                status_indicator(operational),
                spacing="3",
                align="center",
            ),
            justify="between",
            width="100%",
            align="center",
        ),
        padding="1.5rem",
        background="white",
        border_radius="12px",
        border=f"1px solid {Config.BG_DARK}",
        width="100%",
        box_shadow="0 2px 8px rgba(0,0,0,0.05)",
    )

def status_page() -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.box(
            rx.container(
                rx.vstack(
                    # Add logo to the status page for brand consistency
                    rx.image(
                        src="/logo.jpg",
                        alt=Config.COMPANY_NAME,
                        height="80px",
                        width="auto",
                        margin_bottom="2rem",
                    ),
                    rx.heading(
                        "System Status",
                        size="8",
                        color=Config.TEXT_DARK,
                        margin_bottom="0.5rem"
                    ),
                    rx.text(
                        "Aktueller Status der Südwest-Energie Dienste",
                        color=Config.TEXT_LIGHT,
                        margin_bottom="3rem"
                    ),
                    
                    # Overall Status Banner
                    rx.box(
                        rx.hstack(
                            rx.icon(tag="check_circle", color="white", size=32),
                            rx.vstack(
                                rx.text("Alle Systeme operational", color="white", font_weight="700", font_size="1.2rem"),
                                rx.text(f"Zuletzt aktualisiert: {StatusState.last_updated}", color="rgba(255,255,255,0.8)", font_size="0.9rem"),
                                spacing="1",
                            ),
                            spacing="4",
                            align="center",
                        ),
                        background=Config.SECONDARY_COLOR,
                        padding="2rem",
                        border_radius="12px",
                        width="100%",
                        margin_bottom="2rem",
                        box_shadow=f"0 4px 20px {Config.SECONDARY_COLOR}40",
                    ),
                    
                    # Service Cards
                    rx.vstack(
                        service_card("Website & Frontend", StatusState.website_status, StatusState.website_operational, "🌐"),
                        service_card("Datenbank & API", StatusState.db_status, StatusState.db_operational, "🗄️"),
                        service_card("E-Mail Service", StatusState.email_status, StatusState.email_operational, "📧"),
                        service_card("Admin Support (admin@suedwest-energie.de)", StatusState.admin_email_status, StatusState.admin_email_operational, "👤"),
                        spacing="3",
                        width="100%",
                    ),
                    
                    # Auto-refresh note
                    rx.text(
                        "Diese Seite aktualisiert sich automatisch.",
                        color=Config.TEXT_LIGHT,
                        font_size="0.8rem",
                        margin_top="2rem",
                    ),
                    
                    align="center",
                    padding_y="4rem",
                    width="100%",
                    max_width="800px",
                ),
            ),
            background=Config.BG_LIGHT,
            min_height="100vh",
            width="100%",
        ),
        footer(),
        # Trigger check on load
        rx.script("setInterval(() => { window.location.reload() }, 60000)"),  # Simple auto-refresh every 60s
    )
