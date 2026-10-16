"""
pages/4_Riwayat.py — Riwayat Sesi Konsultasi (Enterprise SaaS Dark UI)
"""
import streamlit as st
import sys
from pathlib import Path

# Setup path root
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ui_theme import setup_page, render_hero, clean_html

setup_page("Riwayat Rekomendasi", icon="📜")

# ==============================================================================
# HERO BANNER
# ==============================================================================
render_hero(
    title="Riwayat Sesi Konsultasi",
    subtitle="Log riwayat inferensi yang dijalankan selama sesi browser aktif. Data disimpan di session memory klien dan terhapus otomatis saat logout.",
    badge_text="SESSION AUDIT LOG"
)

riwayat = st.session_state.get("riwayat", [])

if not riwayat:
    empty_html = """
<div class="saas-card" style="text-align: center; padding: 2.5rem 1.5rem;">
<span style="font-size: 2.5rem;">📭</span>
<h3 style="margin: 0.75rem 0 0.35rem 0; font-size: 1.25rem; font-weight: 800; color: #f8f9fa;">Belum Ada Riwayat Sesi</h3>
<p style="color: #9ea3c0; font-size: 0.92rem; margin-bottom: 1.5rem;">
Anda belum menjalankan konsultasi inferensi dalam sesi ini.
</p>
</div>
"""
    st.markdown(clean_html(empty_html), unsafe_allow_html=True)
    
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        if st.button("🔍 Mulai Konsultasi Sekarang", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Rekomendasi.py")
else:
    count_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
<span style="font-size: 0.95rem; color: #f8f9fa; font-weight: 700;">
Total Riwayat Inferensi: <strong style="color: #dee263;">{len(riwayat)}</strong> Kueri
</span>
</div>
"""
    st.markdown(clean_html(count_html), unsafe_allow_html=True)

    # Tampilkan dari yang paling baru
    for i, entry in enumerate(reversed(riwayat), 1):
        idx_label = len(riwayat) - i + 1
        with st.expander(
            f"#{idx_label} &bull; {entry.get('timestamp', '-')} &bull; {entry.get('kebutuhan_label', '-')}",
            expanded=(i == 1)
        ):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Kebutuhan:** `{entry.get('kebutuhan_label', '-')}`")
            with col2:
                st.markdown(f"**Batas Anggaran:** `{entry.get('kelas_label', '-')}`")
            with col3:
                res_count_html = f"<span style='color: #dee263; font-weight: 700;'>{entry.get('jumlah_hasil', 0)} Unit Laptop</span>"
                st.markdown(f"**Hasil:** {res_count_html}", unsafe_allow_html=True)
            
            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
            if entry.get('jumlah_hasil', 0) > 0:
                top_res_html = f"<span style='color: #f8f9fa; font-weight: 700;'>{entry.get('hasil_teratas', '-')}</span>"
                st.markdown(f"**Rekomendasi Utama (Terjangkau):** {top_res_html}", unsafe_allow_html=True)
            else:
                st.markdown("**Hasil:** *Tidak ada unit laptop yang memenuhi seluruh aturan.*")
            
            if entry.get('preferensi'):
                pref_badges = " ".join([f"<span class='badge-spec-pill'>{p}</span>" for p in entry['preferensi']])
                st.markdown(f"**Filter Preferensi Tambahan:** {pref_badges}", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Seluruh Riwayat Sesi", type="secondary"):
        st.session_state['riwayat'] = []
        st.success("Riwayat sesi berhasil dibersihkan.")
        st.rerun()
