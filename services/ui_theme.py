"""
services/ui_theme.py — Design System Core & Remastered SaaS Dark UI for LaptopExpert
Enterprise-grade dark mode dashboard with Indigo (#50579f) & Electric Lime (#dee263) design tokens.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from services.auth_service import is_authenticated, is_admin, get_current_user, logout


# ==============================================================================
# DESIGN TOKENS & COLOR PALETTE
# ==============================================================================
THEME_TOKENS = {
    "brand_primary": "#50579f",             # Deep Indigo / Violet
    "brand_primary_dark": "#3e4482",        # Darker Indigo for gradients
    "brand_primary_light": "#6b73c2",       # Lighter Indigo
    "highlight_accent": "#dee263",          # Vibrant Acid Green / Electric Lime
    "highlight_accent_glow": "rgba(222, 226, 99, 0.5)",
    "bg_deep": "#0b0d14",                   # Obsidian Dark
    "sidebar_bg": "#0e1019",                # Solid Deep Sidebar
    "surface_card": "#131622",              # Dark Slate Surface
    "surface_hover": "#1a1e30",             # Slate Hover
    "border_card": "1px solid rgba(80, 87, 159, 0.35)",
    "border_hover": "rgba(222, 226, 99, 0.5)",
    "text_primary": "#f8f9fa",              # Crisp White
    "text_secondary": "#9ea3c0",            # Cool Gray
    "code_bg": "rgba(15, 17, 26, 0.85)",    # Dark Terminal Monospace
    "code_text": "#dee263",                 # Lime Monospace Text
    "alert_amber_bg": "rgba(245, 158, 11, 0.08)",
    "alert_amber_border": "rgba(245, 158, 11, 0.4)",
}


def clean_html(html: str) -> str:
    """
    Membersihkan leading whitespace dan baris kosong di setiap baris HTML.
    Mencegah parser CommonMark / Markdown Streamlit memperlakukan indentasi >= 4 spasi
    sebagai verbatim code block (<pre><code>).
    """
    return "\n".join(line.strip() for line in html.strip().splitlines() if line.strip())


def inject_custom_css() -> None:
    """Menginjeksi CSS Global Design System tingkat lanjut (Dark Mode Enterprise)."""
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --brand-primary: #50579f;
    --brand-primary-dark: #3e4482;
    --brand-primary-light: #6b73c2;
    --highlight-accent: #dee263;
    --highlight-glow: rgba(222, 226, 99, 0.45);
    --bg-deep: #0b0d14;
    --sidebar-bg: #0e1019;
    --surface-card: #131622;
    --surface-hover: #1a1e30;
    --border-card: 1px solid rgba(80, 87, 159, 0.35);
    --border-hover: rgba(222, 226, 99, 0.5);
    --text-primary: #f8f9fa;
    --text-secondary: #9ea3c0;
    --code-bg: rgba(15, 17, 26, 0.85);
    --code-text: #dee263;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #f8f9fa !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

[data-testid="stSidebarNav"] { display: none !important; }
ul[data-testid="stSidebarNavItems"] { display: none !important; }

.stApp {
    background-color: #0b0d14 !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(80, 87, 159, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(222, 226, 99, 0.05) 0px, transparent 50%);
    background-attachment: fixed;
}

.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1240px !important;
}

header[data-testid="stHeader"] {
    background: rgba(11, 13, 20, 0.8) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid rgba(80, 87, 159, 0.25) !important;
}

/* SIDEBAR STYLING */
section[data-testid="stSidebar"] {
    background-color: #0e1019 !important;
    border-right: 1px solid rgba(80, 87, 159, 0.3) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.6) !important;
}

section[data-testid="stSidebar"] * {
    color: #f8f9fa !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    background-color: #131622 !important;
    border: 1px solid rgba(80, 87, 159, 0.28) !important;
    border-radius: 12px !important;
    padding: 0.65rem 0.95rem !important;
    margin-bottom: 0.5rem !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background-color: #1a1e30 !important;
    border-color: #50579f !important;
    box-shadow: 0 0 14px rgba(80, 87, 159, 0.35) !important;
    transform: translateX(4px) !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] span,
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p {
    color: #f8f9fa !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
}

section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:has([aria-current="page"]) {
    border-left: 3.5px solid #dee263 !important;
    border-color: rgba(222, 226, 99, 0.5) !important;
    background: linear-gradient(90deg, rgba(80, 87, 159, 0.35) 0%, #131622 100%) !important;
}

.sidebar-logout-btn button {
    background-color: rgba(239, 68, 68, 0.1) !important;
    color: #fca5a5 !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}
.sidebar-logout-btn button:hover {
    background-color: rgba(239, 68, 68, 0.25) !important;
    border-color: #ef4444 !important;
    color: #ffffff !important;
    box-shadow: 0 0 12px rgba(239, 68, 68, 0.4) !important;
}

/* FORM ELEMENTS */
div[data-baseweb="select"] > div {
    background-color: #131622 !important;
    border: 1px solid #50579f !important;
    border-radius: 12px !important;
    color: #f8f9fa !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {
    border-color: #dee263 !important;
    box-shadow: 0 0 12px rgba(222, 226, 99, 0.35) !important;
}
div[data-baseweb="select"] * {
    color: #f8f9fa !important;
}

div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #131622 !important;
    border: 1px solid rgba(80, 87, 159, 0.6) !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7) !important;
}
li[role="option"] {
    color: #f8f9fa !important;
    background-color: transparent !important;
    padding: 0.6rem 1rem !important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: #1a1e30 !important;
    color: #dee263 !important;
}

div[data-testid="stRadio"] label { color: #f8f9fa !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label div[data-checked="true"] > div {
    background-color: #dee263 !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label div[data-checked="true"] {
    border-color: #dee263 !important;
    box-shadow: 0 0 8px rgba(222, 226, 99, 0.5) !important;
}

div[data-testid="stCheckbox"] label span {
    color: #f8f9fa !important;
    font-weight: 500;
}
div[data-testid="stCheckbox"] input:checked + div,
div[data-testid="stCheckbox"] div[data-checked="true"] {
    background-color: #50579f !important;
    border-color: #dee263 !important;
    box-shadow: 0 0 8px rgba(222, 226, 99, 0.4) !important;
}

input[type="text"], input[type="password"], textarea {
    background-color: #131622 !important;
    color: #f8f9fa !important;
    border: 1px solid #50579f !important;
    border-radius: 12px !important;
    padding: 0.6rem 0.9rem !important;
    transition: all 0.2s ease !important;
}
input[type="text"]:focus, input[type="password"]:focus, textarea:focus {
    border-color: #dee263 !important;
    box-shadow: 0 0 12px rgba(222, 226, 99, 0.4) !important;
    outline: none !important;
}

/* BUTTONS */
button[data-testid="baseButton-primary"],
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #50579f 0%, #3e4482 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    border: 1px solid rgba(80, 87, 159, 0.8) !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.4rem !important;
    box-shadow: 0 4px 16px rgba(80, 87, 159, 0.35) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
button[data-testid="baseButton-primary"]:hover,
.stButton > button[kind="primary"]:hover {
    border-color: #dee263 !important;
    box-shadow: 0 0 20px rgba(222, 226, 99, 0.5), 0 4px 20px rgba(80, 87, 159, 0.6) !important;
    transform: translateY(-2px) !important;
}

button[data-testid="baseButton-secondary"],
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #dee263 !important;
    font-weight: 600 !important;
    border: 1px solid #50579f !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.4rem !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
button[data-testid="baseButton-secondary"]:hover,
.stButton > button[kind="secondary"]:hover {
    background-color: rgba(80, 87, 159, 0.18) !important;
    border-color: #dee263 !important;
    box-shadow: 0 0 14px rgba(222, 226, 99, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* TABS ACTIVE GLOW */
div[data-baseweb="tab-list"] {
    border-bottom: 1px solid rgba(80, 87, 159, 0.3) !important;
    background-color: transparent !important;
    gap: 0.5rem !important;
}
button[data-baseweb="tab"] {
    color: #9ea3c0 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 1.4rem !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s ease !important;
}
button[data-baseweb="tab"]:hover {
    color: #f8f9fa !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
    font-weight: 800 !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: #dee263 !important;
    height: 3.5px !important;
    border-radius: 4px !important;
    box-shadow: 0 0 12px rgba(222, 226, 99, 0.8) !important;
}

/* TABLES & DATAFRAME */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background-color: #131622 !important;
    border: 1px solid rgba(80, 87, 159, 0.35) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}
div[data-testid="stDataFrame"] div[role="columnheader"] {
    background-color: #1a1e30 !important;
    color: #f8f9fa !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #50579f !important;
}
div[data-testid="stDataFrame"] div[role="row"]:nth-child(even) {
    background-color: #131622 !important;
}
div[data-testid="stDataFrame"] div[role="row"]:nth-child(odd) {
    background-color: #0e1019 !important;
}
div[data-testid="stDataFrame"] * {
    color: #f8f9fa !important;
}

/* MONOSPACE CODE & EXPANDER */
code, pre, [data-testid="stCodeBlock"] {
    font-family: 'JetBrains Mono', monospace !important;
    background-color: rgba(15, 17, 26, 0.85) !important;
    color: #dee263 !important;
    border: 1px solid rgba(80, 87, 159, 0.35) !important;
    border-radius: 10px !important;
}

div[data-testid="stExpander"] {
    background-color: #131622 !important;
    border: 1px solid rgba(80, 87, 159, 0.35) !important;
    border-radius: 14px !important;
    margin-bottom: 0.75rem !important;
}
div[data-testid="stExpander"] summary {
    color: #f8f9fa !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
div[data-testid="stExpander"] summary:hover {
    color: #dee263 !important;
}
div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    border-top: 1px solid rgba(80, 87, 159, 0.25) !important;
    padding: 1rem !important;
}

[data-testid="stMetricValue"] {
    color: #dee263 !important;
    font-weight: 800 !important;
    font-size: 1.85rem !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMetricLabel"] {
    color: #9ea3c0 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

.saas-card {
    background-color: #131622;
    border: 1px solid rgba(80, 87, 159, 0.35);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.saas-card:hover {
    background-color: #1a1e30;
    border-color: rgba(222, 226, 99, 0.5);
    box-shadow: 0 0 20px rgba(222, 226, 99, 0.15), 0 12px 32px rgba(0, 0, 0, 0.5);
}

.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.badge-dedicated {
    background: rgba(222, 226, 99, 0.15);
    color: #dee263;
    border: 1px solid rgba(222, 226, 99, 0.5);
}
.badge-unified {
    background: rgba(80, 87, 159, 0.25);
    color: #c0c6ff;
    border: 1px solid rgba(80, 87, 159, 0.6);
}
.badge-integrated {
    background: rgba(158, 163, 192, 0.12);
    color: #9ea3c0;
    border: 1px solid rgba(158, 163, 192, 0.3);
}
.badge-spec-pill {
    background: rgba(15, 17, 26, 0.85);
    color: #dee263;
    border: 1px solid rgba(80, 87, 159, 0.4);
    padding: 4px 10px;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


def setup_page(
    title: str,
    icon: str = "💻",
    admin_only: bool = False,
    layout: str = "wide"
) -> None:
    """Setup halaman Streamlit dengan konfigurasi modern enterprise dark mode & sesi."""
    st.set_page_config(
        page_title=f"{title} — LaptopExpert SaaS",
        page_icon=icon,
        layout=layout,
        initial_sidebar_state="expanded"
    )
    
    inject_custom_css()
    
    if not is_authenticated():
        st.warning("⚠️ Sesi Anda belum aktif. Silakan login terlebih dahulu.")
        st.page_link("app.py", label="Menuju Halaman Login", icon="🔐")
        st.stop()
    
    if admin_only and not is_admin():
        st.error("🚫 **Akses Terbatas** — Halaman ini dikhususkan untuk Administrator.")
        st.page_link("pages/1_Dashboard.py", label="Kembali ke Dashboard", icon="🏠")
        st.stop()
    
    render_sidebar()


def render_sidebar() -> None:
    """Render sidebar navigasi modern kelas enterprise dark mode."""
    user = get_current_user()
    if not user:
        return
    
    with st.sidebar:
        html_header = """
<div style="padding: 0.5rem 0 1.25rem 0; border-bottom: 1px solid rgba(80, 87, 159, 0.3); margin-bottom: 1.25rem;">
<div style="display: flex; align-items: center; gap: 14px;">
<div style="width: 48px; height: 48px; background: linear-gradient(135deg, #50579f 0%, #3e4482 100%); border: 1px solid rgba(222, 226, 99, 0.5); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 0 16px rgba(80, 87, 159, 0.4);">💻</div>
<div>
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #f8f9fa; letter-spacing: -0.02em;">LaptopExpert</h3>
<div style="display: inline-flex; align-items: center; gap: 6px; margin-top: 3px;">
<span style="width: 7px; height: 7px; background-color: #dee263; border-radius: 50%; box-shadow: 0 0 8px #dee263;"></span>
<span style="font-size: 0.72rem; font-weight: 700; color: #dee263; letter-spacing: 0.04em;">PROLOG ENGINE ACTIVE</span>
</div>
</div>
</div>
</div>
"""
        st.markdown(clean_html(html_header), unsafe_allow_html=True)
        
        is_adm = user['role'] == 'admin'
        role_label = "👑 ENTERPRISE ADMIN" if is_adm else "🎓 MAHASISWA VERIFIED"
        role_badge_bg = "rgba(222, 226, 99, 0.12)" if is_adm else "rgba(80, 87, 159, 0.25)"
        role_border = "rgba(222, 226, 99, 0.4)" if is_adm else "rgba(80, 87, 159, 0.5)"
        role_text_color = "#dee263" if is_adm else "#c0c6ff"
        
        html_user = f"""
<div style="background: {role_badge_bg}; border: 1px solid {role_border}; border-radius: 14px; padding: 12px 14px; margin-bottom: 1.5rem; box-shadow: inset 0 1px 1px rgba(255,255,255,0.05);">
<div style="font-size: 0.7rem; font-weight: 800; color: {role_text_color}; letter-spacing: 0.05em; text-transform: uppercase;">{role_label}</div>
<div style="font-size: 1.05rem; font-weight: 800; color: #f8f9fa; margin-top: 2px;">{user['nama']}</div>
<div style="font-size: 0.75rem; color: #9ea3c0; margin-top: 2px;">User ID: @{user['username']}</div>
</div>
"""
        st.markdown(clean_html(html_user), unsafe_allow_html=True)
        
        html_menu_title = """
<p style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #9ea3c0; letter-spacing: 0.08em; margin-bottom: 0.75rem;">
PORTAL NAVIGASI
</p>
"""
        st.markdown(clean_html(html_menu_title), unsafe_allow_html=True)
        
        st.page_link("pages/1_Dashboard.py", label="Dashboard Utama", icon="🏠")
        st.page_link("pages/2_Rekomendasi.py", label="Konsultasi Rekomendasi", icon="🔍")
        
        if is_adm:
            st.page_link("pages/3_Basis_Pengetahuan.py", label="Basis Pengetahuan (Admin)", icon="📚")
        
        st.page_link("pages/4_Riwayat.py", label="Riwayat Konsultasi", icon="📜")
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown('<div class="sidebar-logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Keluar Akun (Logout)", use_container_width=True):
            logout()
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# REUSABLE UI COMPONENTS (ENTERPRISE SAAS MODERN)
# ==============================================================================

def render_hero(
    title: str,
    subtitle: str,
    badge_text: str = "SISTEM PAKAR PROLOG",
    role: Optional[str] = None
) -> None:
    """Hero banner modern dengan aksen gradient sudut halus dan badge neon."""
    role_markup = f'<span style="background: rgba(222, 226, 99, 0.15); color: #dee263; border: 1px solid rgba(222, 226, 99, 0.4); padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; margin-left: 8px;">{role}</span>' if role else ""
    
    html = f"""
<div style="background: linear-gradient(135deg, rgba(80, 87, 159, 0.28) 0%, rgba(19, 22, 34, 0.95) 60%, rgba(11, 13, 20, 0.98) 100%); border: 1px solid rgba(80, 87, 159, 0.4); border-radius: 20px; padding: 2.25rem 2.25rem; margin-bottom: 2rem; position: relative; overflow: hidden; box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);">
<div style="position: absolute; top: -40px; right: -40px; width: 180px; height: 180px; background: radial-gradient(circle, rgba(222, 226, 99, 0.15) 0%, transparent 70%); border-radius: 50%;"></div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
<span style="background: rgba(80, 87, 159, 0.35); color: #c0c6ff; border: 1px solid rgba(80, 87, 159, 0.6); padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">{badge_text}</span>
{role_markup}
</div>
<h1 style="color: #f8f9fa; margin: 0 0 0.5rem 0; font-size: 2.15rem; font-weight: 800; letter-spacing: -0.025em; line-height: 1.2;">{title}</h1>
<p style="color: #9ea3c0; font-size: 1.02rem; max-width: 820px; margin: 0; line-height: 1.6;">{subtitle}</p>
</div>
"""
    st.markdown(clean_html(html), unsafe_allow_html=True)


def render_metric_card(
    title: str,
    value: Any,
    icon: str = "📊",
    caption: str = ""
) -> None:
    """Stat card kaca transparan dengan angka besar warna #dee263."""
    caption_markup = f'<div style="font-size: 0.76rem; color: #9ea3c0; margin-top: 4px;">{caption}</div>' if caption else ""
    html = f"""
<div style="background-color: #131622; border: 1px solid rgba(80, 87, 159, 0.35); border-radius: 16px; padding: 1.4rem 1.5rem; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3); transition: all 0.25s ease;">
<div style="display: flex; justify-content: space-between; align-items: flex-start;">
<span style="font-size: 0.82rem; font-weight: 700; color: #9ea3c0; text-transform: uppercase; letter-spacing: 0.04em;">{title}</span>
<span style="font-size: 1.4rem;">{icon}</span>
</div>
<div style="font-size: 2.25rem; font-weight: 800; color: #dee263; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0.35rem 0 0.1rem 0; letter-spacing: -0.03em;">{value}</div>
{caption_markup}
</div>
"""
    st.markdown(clean_html(html), unsafe_allow_html=True)


def render_laptop_card(
    laptop: Dict[str, Any],
    alasan: str = "",
    show_prolog_rule: bool = False,
    kebutuhan: str = ""
) -> None:
    """
    Kartu model laptop konkret bergaya catalog card e-commerce modern:
    - Card surface #131622 dengan border violet dan glow hover #dee263
    - Badge RAM/SSD/GPU berdesain pill
    - Teks monospace untuk chipset
    - Alasan XAI dan Prolog trace terintegrasi rapi
    """
    gpu_badge_str = laptop.get('gpu_badge', '⚪ Integrated')
    if 'Dedicated' in gpu_badge_str:
        badge_cls = 'badge-dedicated'
    elif 'Unified' in gpu_badge_str:
        badge_cls = 'badge-unified'
    else:
        badge_cls = 'badge-integrated'

    merk_icon = laptop.get('merk_icon', '💻')
    display_name = laptop.get('display_name', f"{laptop.get('merk', '').capitalize()} {laptop.get('model', '')}")
    cpu_val = laptop.get('cpu', '-')
    ram_val = laptop.get('ram', '-')
    storage_val = laptop.get('storage', '-')
    vga_val = laptop.get('vga', '-')
    harga_display = laptop.get('harga_display', f"Rp {laptop.get('harga_juta', 0)} Jt")
    
    html_card = f"""
<div style="background-color: #131622; border: 1px solid rgba(80, 87, 159, 0.35); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35); transition: all 0.25s ease;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 1rem;">
<div>
<div style="display: flex; align-items: center; gap: 8px;">
<span style="font-size: 1.3rem;">{merk_icon}</span>
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #f8f9fa;">{display_name}</h3>
</div>
<div style="margin-top: 4px; font-size: 0.85rem; color: #9ea3c0;">
Prosesor: <span style="color: #dee263; font-family: 'JetBrains Mono', monospace; font-weight: 600;">{cpu_val}</span>
</div>
</div>
<div style="text-align: right; background: rgba(80, 87, 159, 0.18); border: 1px solid rgba(80, 87, 159, 0.4); padding: 6px 14px; border-radius: 12px;">
<div style="font-size: 0.68rem; font-weight: 700; color: #9ea3c0; text-transform: uppercase;">Estimasi Harga</div>
<div style="font-size: 1.25rem; font-weight: 800; color: #dee263; font-family: 'Plus Jakarta Sans', sans-serif;">{harga_display}</div>
</div>
</div>
<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 0.5rem;">
<div class="badge-spec-pill">💾 {ram_val} GB RAM</div>
<div class="badge-spec-pill">⚡ {storage_val} GB SSD</div>
<span class="badge-pill {badge_cls}">{gpu_badge_str}</span>
<div class="badge-spec-pill" style="color: #9ea3c0;">🎮 {vga_val}</div>
</div>
</div>
"""
    st.markdown(clean_html(html_card), unsafe_allow_html=True)
    
    if alasan:
        html_alasan = f"""
<div style="background-color: rgba(15, 17, 26, 0.85); border: 1px solid rgba(80, 87, 159, 0.3); border-left: 3px solid #dee263; border-radius: 10px; padding: 12px 16px; margin: -0.5rem 0 1rem 0;">
<div style="font-size: 0.74rem; font-weight: 800; color: #dee263; text-transform: uppercase; letter-spacing: 0.04em;">💡 Justifikasi Sistem Pakar</div>
<div style="font-size: 0.88rem; color: #f8f9fa; margin-top: 4px; line-height: 1.5;">{alasan}</div>
</div>
"""
        st.markdown(clean_html(html_alasan), unsafe_allow_html=True)
        
    if show_prolog_rule and kebutuhan:
        with st.expander("🔍 Trace Logika Deduksi Prolog"):
            rule_syntax = (
                f"% Goal Resolusi Orde Pertama:\n"
                f"?- rekomendasi_ideal({kebutuhan}, Kelas, {laptop.get('merk', 'merk')}, "
                f"'{laptop.get('model', 'model')}', {ram_val}, '{vga_val}', {laptop.get('harga_juta', 0)})."
            )
            st.code(rule_syntax, language="prolog")
            html_trace = f"""
<div style="font-size: 0.78rem; color: #dee263; font-family: 'JetBrains Mono', monospace; margin-top: 4px;">
✔ Predikat <code>cocok_untuk(ID, {kebutuhan})</code> bernilai TRUE<br>
✔ Predikat <code>kelas_laptop(ID, Kelas)</code> konsisten dengan batas anggaran
</div>
"""
            st.markdown(clean_html(html_trace), unsafe_allow_html=True)


def render_compromise_alert(message: str, tips: List[str] = None) -> None:
    """Alert container beraksen amber/gold dengan outline rapi."""
    tips_markup = ""
    if tips:
        items = "".join([f"<li style='margin-bottom: 4px;'>{t}</li>" for t in tips])
        tips_markup = f"""
<div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(245, 158, 11, 0.25);">
<div style="font-weight: 700; font-size: 0.85rem; color: #fde68a; margin-bottom: 6px;">💡 Tips Alternatif Solusi:</div>
<ul style="margin: 0; padding-left: 1.25rem; font-size: 0.85rem; color: #f8f9fa;">{items}</ul>
</div>
"""
        
    html = f"""
<div style="background-color: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.45); border-radius: 14px; padding: 1.25rem 1.5rem; margin: 1rem 0; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);">
<div style="display: flex; align-items: flex-start; gap: 12px;">
<span style="font-size: 1.4rem;">⚠️</span>
<div style="flex: 1;">
<div style="font-weight: 800; font-size: 0.95rem; color: #fde68a; letter-spacing: 0.02em;">KOMPROMI ATURAN INFERENSI</div>
<div style="font-size: 0.9rem; color: #f8f9fa; margin-top: 4px; line-height: 1.5;">{message}</div>
{tips_markup}
</div>
</div>
</div>
"""
    st.markdown(clean_html(html), unsafe_allow_html=True)


def render_specs_comparison(min_specs: List[str], ideal_specs: List[str]) -> None:
    """
    Specs Comparison Grid (Minimum vs Ideal):
    - Ambang Minimum: Border #50579f dengan badge 'SYARAT MINIMUM'
    - Konfigurasi Ideal: Border aksen #dee263 dengan badge 'PERFORMA MAKSIMAL' berteks neon
    """
    c_min, c_ideal = st.columns(2)
    
    with c_min:
        min_items = "".join([
            f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 0.88rem; color: #f8f9fa;'>"
            f"<span style='color: #6b73c2; font-weight: 800;'>▪</span> {sp}</div>" 
            for sp in min_specs
        ])
        html_min = f"""
<div style="background-color: #131622; border: 1.5px solid #50579f; border-radius: 16px; padding: 1.4rem; height: 100%; box-shadow: 0 4px 20px rgba(80, 87, 159, 0.2);">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
<span style="font-size: 1rem; font-weight: 800; color: #f8f9fa;">📋 Ambang Minimum</span>
<span style="background: rgba(80, 87, 159, 0.25); color: #c0c6ff; border: 1px solid #50579f; padding: 4px 10px; border-radius: 9999px; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.04em;">SYARAT MINIMUM</span>
</div>
<div style="line-height: 1.6;">{min_items}</div>
</div>
"""
        st.markdown(clean_html(html_min), unsafe_allow_html=True)
        
    with c_ideal:
        ideal_items = "".join([
            f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 0.88rem; color: #f8f9fa;'>"
            f"<span style='color: #dee263; font-weight: 800;'>⚡</span> {sp}</div>" 
            for sp in ideal_specs
        ])
        html_ideal = f"""
<div style="background-color: #131622; border: 1.5px solid #dee263; border-radius: 16px; padding: 1.4rem; height: 100%; box-shadow: 0 0 24px rgba(222, 226, 99, 0.25);">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
<span style="font-size: 1rem; font-weight: 800; color: #dee263;">⭐ Konfigurasi Ideal</span>
<span style="background: rgba(222, 226, 99, 0.15); color: #dee263; border: 1px solid #dee263; padding: 4px 10px; border-radius: 9999px; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.04em; box-shadow: 0 0 10px rgba(222, 226, 99, 0.4);">PERFORMA MAKSIMAL</span>
</div>
<div style="line-height: 1.6;">{ideal_items}</div>
</div>
"""
        st.markdown(clean_html(html_ideal), unsafe_allow_html=True)


def render_xai_panel(
    query_info: Dict[str, Any],
    query_str: str,
    rules_fired: List[str],
    justifications: List[str]
) -> None:
    """
    Explainable AI (XAI) Panel beraksen dark terminal/IDE:
    - Rantai fakta sesi (kebutuhan_pengguna, kelas_anggaran, dll.)
    - Rules terpicu dalam container bernuansa dark terminal/IDE
    - Format checklist interaktif
    """
    just_items = "".join([
        f"<div style='display: flex; align-items: flex-start; gap: 10px; margin-bottom: 8px; font-size: 0.88rem; color: #f8f9fa;'>"
        f"<span style='color: #dee263; font-weight: 800;'>[✓]</span> <span>{j}</span></div>"
        for j in justifications
    ])
    
    rules_items = "".join([
        f"<div style='color: #c0c6ff; margin-bottom: 4px;'>▶ <code>{r}</code></div>"
        for r in rules_fired
    ])

    html = f"""
<div style="background-color: rgba(15, 17, 26, 0.95); border: 1px solid rgba(80, 87, 159, 0.5); border-radius: 16px; padding: 1.5rem; margin-top: 1.25rem; box-shadow: 0 12px 32px rgba(0,0,0,0.5);">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(80, 87, 159, 0.3); padding-bottom: 0.75rem; margin-bottom: 1rem;">
<div style="display: flex; align-items: center; gap: 6px;">
<span style="width: 10px; height: 10px; border-radius: 50%; background: #ef4444; display: inline-block;"></span>
<span style="width: 10px; height: 10px; border-radius: 50%; background: #f59e0b; display: inline-block;"></span>
<span style="width: 10px; height: 10px; border-radius: 50%; background: #dee263; display: inline-block;"></span>
<span style="margin-left: 10px; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #9ea3c0;">xai_session_trace.pl &bull; Prolog Engine v10.0</span>
</div>
<span style="background: rgba(222, 226, 99, 0.12); color: #dee263; border: 1px solid rgba(222, 226, 99, 0.4); padding: 2px 8px; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">CONFIDENCE: 100% DETERMINISTIC</span>
</div>
<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; margin-bottom: 1.25rem;">
<div style="color: #9ea3c0; margin-bottom: 4px;">// Rantai Fakta & Rule Terpicu:</div>
{rules_items}
</div>
<div style="border-top: 1px solid rgba(80, 87, 159, 0.25); padding-top: 1rem;">
<div style="font-size: 0.85rem; font-weight: 700; color: #dee263; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.75rem;">✔ Butir Pembuktian Teknis (Formal Justification Trace):</div>
{just_items}
</div>
</div>
"""
    st.markdown(clean_html(html), unsafe_allow_html=True)


def render_no_results(kebutuhan_label: str, kelas_label: str) -> None:
    """Tampilan jelas beraksen SaaS dark ketika inferensi tidak menemukan kecocokan."""
    html = f"""
<div style="background-color: #131622; border: 1px solid rgba(80, 87, 159, 0.4); border-radius: 16px; padding: 1.75rem; margin: 1.5rem 0; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0.75rem;">
<span style="font-size: 1.6rem;">⚠️</span>
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #f8f9fa;">Aturan Belum Terpenuhi (No Matching Rules)</h3>
</div>
<p style="color: #9ea3c0; font-size: 0.95rem; line-height: 1.5; margin: 0 0 1rem 0;">
Tidak ditemukan unit laptop dalam basis pengetahuan yang memenuhi beban komputasi <strong style="color: #dee263;">{kebutuhan_label}</strong> pada batas anggaran <strong style="color: #dee263;">{kelas_label}</strong>.
</p>
</div>
"""
    st.markdown(clean_html(html), unsafe_allow_html=True)
    
    render_compromise_alert(
        message="Beban komputasi yang dipilih membutuhkan spesifikasi hardware (misal: GPU Dedicated atau RAM >= 16 GB) yang melampaui plafon kelas anggaran saat ini.",
        tips=[
            "Tingkatkan batas anggaran satu tingkat ke atas untuk menjangkau laptop dengan GPU diskrit.",
            "Turunkan intensitas beban kerja (misal: dari Desain Berat 4K ke Desain Grafis Ringan).",
            "Hapus centang preferensi opsional bila kriteria filter terlalu ketat."
        ]
    )


def render_error_message(error: str) -> None:
    """Tampilkan notifikasi error human-friendly dengan gaya terminal."""
    html = """
<div style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 14px; padding: 1.25rem; margin: 1rem 0;">
<div style="font-weight: 800; color: #fca5a5; font-size: 0.95rem;">❌ Kendala Komunikasi Mesin SWI-Prolog</div>
<div style="color: #f8f9fa; font-size: 0.88rem; margin-top: 4px;">Terjadi kesalahan teknis saat mengevaluasi goal pada mesin inferensi logika.</div>
</div>
"""
    st.markdown(clean_html(html), unsafe_allow_html=True)
    with st.expander("Detail Pesan Error"):
        st.code(error, language="text")
