"""
utils/ui_helpers.py — Bridge & Compatibility Layer for LaptopExpert UI Design System
Re-exports core UI components from services.ui_theme to ensure complete backward compatibility.
"""

from services.ui_theme import (
    setup_page,
    inject_custom_css,
    render_sidebar,
    render_hero,
    render_metric_card,
    render_laptop_card,
    render_compromise_alert,
    render_specs_comparison,
    render_xai_panel,
    render_no_results,
    render_error_message,
    THEME_TOKENS
)

__all__ = [
    "setup_page",
    "inject_custom_css",
    "render_sidebar",
    "render_hero",
    "render_metric_card",
    "render_laptop_card",
    "render_compromise_alert",
    "render_specs_comparison",
    "render_xai_panel",
    "render_no_results",
    "render_error_message",
    "THEME_TOKENS"
]
