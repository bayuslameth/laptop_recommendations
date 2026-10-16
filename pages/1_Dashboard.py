"""
pages/1_Dashboard.py — Dashboard Utama LaptopExpert (Enterprise SaaS Dark UI)
"""
import streamlit as st
import sys
from pathlib import Path

# Setup path root
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ui_theme import (
    setup_page,
    clean_html,
    render_hero,
    render_metric_card,
    render_error_message
)
from services.prolog_engine import get_prolog_engine
from services.auth_service import get_current_user, is_admin

setup_page("Dashboard", icon="🏠")

user = get_current_user()
engine = get_prolog_engine()

# ==============================================================================
# HERO BANNER
# ==============================================================================
render_hero(
    title=f"Selamat Datang, {user['nama']}! 👋",
    subtitle="Temukan rekomendasi spesifikasi laptop paling akurat dan objektif untuk kebutuhan studi Anda melalui evaluasi logika predikat deduktif SWI-Prolog.",
    badge_text="SISTEM PAKAR BERBASIS LOGIKA",
    role="VERIFIED SESSION"
)

# Status Mesin Inferensi
if not engine.is_loaded:
    render_error_message(f"Knowledge Base Prolog Gagal Terhubung: {engine.error_message}")
    st.stop()

# ==============================================================================
# STATISTIK PROLOG (REAL-TIME METRICS)
# ==============================================================================
st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8f9fa; margin-bottom: 0.2rem;'>📊 Statistik Knowledge Base</h3>", unsafe_allow_html=True)
st.caption("Data berikut dihitung secara langsung melalui evaluasi resolusi predikat SWI-Prolog.")

stats = engine.get_stats()

col1, col2, col3 = st.columns(3)

with col1:
    render_metric_card(
        title="Total Laptop Database",
        value=stats.get('laptop', 70),
        icon="💾",
        caption="Fakta spesifikasi/8 aktif"
    )

with col2:
    render_metric_card(
        title="Profil Penggunaan",
        value=stats.get('kategori', 8),
        icon="📋",
        caption="Kategori beban kerja software"
    )

with col3:
    render_metric_card(
        title="Aturan Inferensi Aktif",
        value="12+",
        icon="⚙️",
        caption="Rules cocok_untuk & kelas_laptop"
    )

# Distribusi Kelas Anggaran
st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
dist_header = """
<div class="saas-card" style="padding: 1.25rem 1.5rem; margin-bottom: 0.5rem;">
<div style="font-size: 0.82rem; font-weight: 800; color: #9ea3c0; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.85rem;">
Distribusi Unit Berdasarkan Partisi Kelas Anggaran
</div>
</div>
"""
st.markdown(clean_html(dist_header), unsafe_allow_html=True)

col_e, col_m, col_h, col_f = st.columns(4)
with col_e:
    st.metric("🟢 Entry (< 10 Jt)", f"{stats.get('entry', 0)} Unit")
with col_m:
    st.metric("🔵 Midrange (10 - 19 Jt)", f"{stats.get('midrange', 0)} Unit")
with col_h:
    st.metric("🟣 High-End (20 - 34 Jt)", f"{stats.get('high_end', 0)} Unit")
with col_f:
    st.metric("🟡 Flagship (≥ 35 Jt)", f"{stats.get('flagship', 0)} Unit")

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

# ==============================================================================
# CARA KERJA SISTEM & ACTION CALLOUT
# ==============================================================================
col_desc, col_cta = st.columns([1.8, 1.2])

with col_desc:
    desc_html = """
<div class="saas-card" style="height: 100%;">
<h3 style="margin: 0 0 0.75rem 0; font-size: 1.25rem; font-weight: 800; color: #f8f9fa;">💡 Bagaimana LaptopExpert Bekerja?</h3>
<p style="color: #9ea3c0; font-size: 0.92rem; line-height: 1.6; margin-bottom: 0.75rem;">
Aplikasi ini mengimplementasikan konsep sistem pakar formal dengan pemisahan tegas antara basis pengetahuan (fakta & aturan) dan mesin penarik kesimpulan (inference engine):
</p>
<div style="font-size: 0.88rem; color: #f8f9fa; line-height: 1.7;">
<div style="margin-bottom: 6px;"><strong style="color: #dee263;">1. Knowledge Representation:</strong> 70+ laptop dimodelkan sebagai fakta logika predikat <code>spesifikasi/8</code>, dan syarat hardware software dirumuskan dalam aturan <code>cocok_untuk/2</code>.</div>
<div style="margin-bottom: 6px;"><strong style="color: #dee263;">2. Backward Chaining Resolution:</strong> Saat Anda memulai konsultasi, SWI-Prolog membuktikan goal kueri secara matematis tanpa probabilitas acak.</div>
<div><strong style="color: #dee263;">3. Explainable Output (XAI):</strong> Setiap rekomendasi dilengkapi trace predikat Prolog dan alasan teknis mengapa laptop tersebut memenuhi kriteria.</div>
</div>
</div>
"""
    st.markdown(clean_html(desc_html), unsafe_allow_html=True)

with col_cta:
    cta_html = """
<div class="saas-card" style="text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
<div style="width: 56px; height: 56px; background: rgba(80, 87, 159, 0.25); border: 1px solid rgba(222, 226, 99, 0.4); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin-bottom: 1rem;">
🚀
</div>
<h4 style="margin: 0 0 0.35rem 0; font-size: 1.2rem; font-weight: 800; color: #f8f9fa;">Mulai Konsultasi</h4>
<p style="font-size: 0.88rem; color: #9ea3c0; margin-bottom: 1.5rem; line-height: 1.5;">
Pilih profil beban studi kuliah Anda dan dapatkan rekomendasi laptop yang paling terverifikasi.
</p>
</div>
"""
    st.markdown(clean_html(cta_html), unsafe_allow_html=True)
    
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    if st.button("🔍 Konsultasi Rekomendasi Sekarang", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Rekomendasi.py")
    
    if is_admin():
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
        if st.button("📚 Buka Panel Basis Pengetahuan", use_container_width=True):
            st.switch_page("pages/3_Basis_Pengetahuan.py")
